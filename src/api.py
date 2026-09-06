"""
This module will define the API by defining routes and their allowed methods, etc.
"""
from typing import Annotated, List
import db.schemas as schemas
import models
from db.db_operations import SessionLocal
from sqlalchemy.orm import Session
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

from pipeline import ai_functions, create_recommendations

router = APIRouter()

def get_db():
    """
    get db session
    :yield: the db session:
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# ///////////////// Users specific C.R.U.D. routes ///////////////// #
@router.post("/users/", response_model=models.UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      user: models.UserCreate = Body(
                          description="UserCreate object",
                      )):
    """
    - create a new user
    - :param user: UserCreate object
    - :return db_user: UserResponse object
    """
    new_user = schemas.User(name=user.name if user.name is not None else '',
                            family_name=user.family_name,
                            address=user.address,
                            gps_coordinates=user.gps_coordinates if user.gps_coordinates is not None else '')
    db.add(new_user)
    db.commit()
    return new_user

@router.get("/users/", response_model=List[models.UserResponse])
def read_all_users(db: db_dependency):
    """
    - Get all users.
    - :return users: list of UserResponse objects:
    """
    users = db.query(schemas.User).all()
    if not users or len(users) == 0:
        raise HTTPException(status_code=404, detail="Users not found")
    return users


@router.get("/users/{user_id}", response_model=models.UserResponse)
def get_user(db: db_dependency,
              user_id: int = Path(
                  description="The unique ID of the user",
                  examples=[40451]  # Populates the path input field
              )):
    """
    - Retrieves a user by its ID.
    - :param user_id: unique id of the user (int)
    - :return user: UserResponse object:
    """
    user = db.query(schemas.User).filter(schemas.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users/{user_id}", response_model=models.UserResponse)
async def update_user(db: db_dependency,
                      user_id: Annotated[int,Path(
                          description="The unique ID of the user",
                          examples=[40451]
                      )],
                      user: Annotated[models.UserCreate, Body(
                          description="UserCreate object"
                      )]
    ):
    """
    - update a user, finding it by its ID.
    - :param user_id: unique id of the user (int)
    - :param user: UserCreate object:
    - :return user: UserResponse object:
    """
    db_user = db.get(schemas.User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Get only UserCreate Fields, that actually got send within the request
    user_update = user.model_dump(exclude_unset=True)

    # Map through the dictionary to update the database entry
    for key, value in user_update.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user

@router.delete("/users/{user_id}", response_model=models.UserResponse)
async def delete_user(db: db_dependency,
                      user_id: int = Path(
                          description="The unique ID of the user",
                          examples=[40451]  # Populates the path input field
                      )):
    """
    - delete a user by its ID.
    - :param user_id: unique id of the user (int)
    - :return user: UserResponse object:
    """
    db_user = db.get(schemas.User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return db_user

# ///////////////// End of Users routes ///////////////// #
# ///////////////// Search-histories specific C.R.U.D. routes ///////////////// #
@router.post("/users/{user_id}/searches", response_model=models.SearchResponse, status_code=status.HTTP_201_CREATED)
async def new_search_by_user(db: db_dependency,
                              user_id: Annotated[int,Path(
                                  description="The unique ID of the user",
                                  examples=[40451]
                              )],
                              search: Annotated[models.SearchCreate, Body(
                                  description="SearchCreate object"
                              )]):
    """
    - create a new search from user with user_id.
    - :param user_id: unique id of the user (int)
    - :param search: SearchCreate object
    - :return db_search: SearchResponse object:
    """

    search = schemas.Searchhistory(starting_point=search.starting_point,
                                 distance=float(search.distance),
                                 traveltime=search.traveltime,
                                 theme=search.theme,
                                 transport_type=search.transport_type,
                                 group_size=search.group_size,
                                 user_id=user_id)

    db.add(search)
    db.commit()
    create_recommendations.recommendations_flow(search)
    return search

@router.get('/users/{user_id}/searches', response_model=List[models.SearchResponse])
async def searches_by_user(db: db_dependency,
                   user_id: int = Path(
                       description="The unique ID of the user",
                       examples=[40451]
                   )):
    """
    - searches for all Searches with user_id.
    - :param user_id: unique id of the user (int)
    - :return searches: list of Searches objects:
    """
    searches = db.query(schemas.Searchhistory).filter(schemas.Searchhistory.user_id == user_id).all()
    if not searches:
        raise HTTPException(status_code=404, detail=f"Searches from user with user_id: {user_id} not found")
    return searches

@router.get("/users/{user_id}/searches/{search_id}", response_model=models.SearchResponse)
async def get_search(db: db_dependency,
                      user_id: Annotated[int, Path(
                          description="The unique ID of the user",
                          examples=[40451]
                      )],
                      search_id: Annotated[int, Path(
                          description="The unique ID of the search",
                          examples=[40451]
                      )]
    ):
    """
    - get a search by its ID, from user with user_id.
    - :param user_id: unique id of the user (int)
    - :param search_id: unique id of the search (int)
    - :return db_search: SearchResponse object:
    """
    db_search = db.get(schemas.Searchhistory, search_id)
    if not db_search or db_search.user_id != user_id:
        raise HTTPException(
            status_code=404,
            detail=f"Search with id {search_id} for user with id {user_id} not found"
        )
    return db_search

@router.put("/users/{user_id}/searches/{search_id}", response_model=models.SearchResponse)
async def update_search(db: db_dependency,
                        user_id: Annotated[int,Path(
                            description="The unique ID of the user",
                            examples=[40451]
                        )],
                        search_id: Annotated[int, Path(
                            description="The unique ID of the search",
                            examples=[40451]
                        )],
                        search: Annotated[models.SearchCreate, Body(
                            description="SearchCreate object"
                        )]
    ):
    """
    - update a search by its ID, from user with user_id.
    - :param user_id: unique id of the user (int):
    - :param search_id: SearchCreate object:
    - :param search: SearchCreate object:
    - :return search: SearchResponse object:
    """
    db_search =  db.get(schemas.Searchhistory, search_id)
    if not db_search or db_search.user_id != user_id:
        raise HTTPException(
            status_code=404,
            detail=f"Search with id {search_id} for user with id {user_id} not found"
        )

    # Get only SearchCreate Fields, that actually got send within the request
    search_update = search.model_dump(exclude_unset=True)

    # Map through the dictionary to update the database entry
    for key, value in search_update.items():
        setattr(db_search, key, value)

    db.commit()
    db.refresh(db_search)
    return db_search

@router.delete("/users/{user_id}/searches/{search_id}", response_model=models.SearchResponse)
async def delete_search(db: db_dependency,
                        user_id: Annotated[int,Path(
                            description="The unique ID of the user",
                            examples=[40451]
                        )],
                        search_id: Annotated[int, Path(
                            description="The unique ID of the search",
                            examples=[40451]
                        )]
    ):
    """
    - delete a search by its ID, from user with user_id.
    - :param user_id: unique id of the user (int):
    - :param search_id: unique id of the search (int):
    - :return db_search: SearchResponse object:
    """
    db_search = db.get(schemas.Searchhistory, search_id)
    if not db_search or db_search.user_id != user_id:
        raise HTTPException(
            status_code=404,
            detail=f"Search with id {search_id} for user with id {user_id} not found"
        )
    db.delete(db_search)
    db.commit()
    return db_search

# ///////////////// End of Search-histories routes ///////////////// #
# ///////////////// Suggestions specific C.R.U.D. routes ///////////////// #
@router.post("/users/{user_id}/{search_id}/suggestions",
             response_model=List[models.SuggestionResponse],
             status_code=status.HTTP_201_CREATED)
async def create_suggestions(db: db_dependency,
                             user_id: Annotated[int,Path(
                                 description="The unique ID of the user",
                                 examples=[40451]
                             )],
                             search_id: Annotated[int, Path(
                                 description="The unique ID of the search",
                                 examples=[40451]
                             )],
                             suggestions: Annotated[List[models.SuggestionCreate], Body(
                                 description="List of SuggestionCreate object/s."
                             )]
    ):
    """
    - create suggestions for search with search_id, from user with user_id.
    - :param user_id: unique id of the user (int):
    - :param search_id: unique id of the search (int):
    - :param suggestions: List of SuggestionCreate object/s:
    - :return suggestions: List of SuggestionResponse object/s:
    """
    suggestion_list = []
    for suggestion in suggestions:
        db_suggestion = schemas.Suggestion(
            title=suggestion.title,
            description=suggestion.description,
            est_trip_costs=suggestion.est_trip_costs,
            sug_transport_type=suggestion.sug_transport_type,
            destination_coordinates=suggestion.destination_coordinates if suggestion.destination_coordinates else '',
            user_id=user_id,
            history_id=search_id
        )
        db.add(db_suggestion)
        db.commit()
        suggestion_list.append(db_suggestion)
    return suggestion_list


@router.get("/users/{user_id}/suggestions", response_model=List[models.SuggestionResponse])
async def get_suggestions(db: db_dependency,
                          user_id: Annotated[int,Path(
                              description="The unique ID of the user",
                              examples=[40451]
                          )],
    ):
    """
    - get suggestions for search with search_id, from user with user_id.
    - :param user_id: unique id of the user (int):
    - :param search_id: unique id of the search (int):
    - :return db_suggestions: SuggestionResponse object:
    """
    db_suggestions = db.query(schemas.Suggestion).filter(schemas.Suggestion.user_id == user_id).all()
    if not db_suggestions:
        raise HTTPException(status_code=404, detail=f"Suggestions for user with user_id {user_id} not found")
    return db_suggestions

@router.get("/user/{user_id}/suggestion/{suggestion_id}", response_model=models.SuggestionResponse)
async def get_suggestion(db: db_dependency,
                         user_id: Annotated[int,Path(
                             description="The unique ID of the user",
                             examples=[40451]
                         )],
                         suggestion_id: Annotated[int, Path(
                             description="The unique ID of the suggestion",
                             examples=[40451]
                         )]
    ):
    """
    - get suggestion by it ID for search with search_id, from user with user_id.
    - :param user_id: unique id of the user (int):
    - :param search_id: unique id of the search (int):
    - :param suggestion_id: unique id of the suggestion (int):
    - :return db_suggestion: SuggestionResponse object:
    """
    db_suggestion = db.get(schemas.Suggestion, suggestion_id)
    if not db_suggestion or db_suggestion.user_id != user_id:
        raise HTTPException(
            status_code=404,
            detail=f"Suggestion with suggestion_id {suggestion_id} for user with user_id {user_id} not found"
        )
    return db_suggestion


@router.put("/users/{user_id}/suggestions/{suggestion_id}", response_model=models.SuggestionResponse)
async def update_suggestion(db: db_dependency,
                            user_id: Annotated[int,Path(
                                description="The unique ID of the user",
                                examples=[40451]
                            )],
                            suggestion_id: Annotated[int, Path(
                                description="The unique ID of the suggestion",
                                examples=[40451]
                            )],
                            suggestion: Annotated[models.SuggestionCreate, Body(
                                description="SuggestionCreate object/s."
                            )]
    ):
    """
    - update suggestion with suggestion_id, from user with user_id of search-history with search_id.
    - :param user_id: unique id of the user (int):
    - :param search_id: unique id of the search (int):
    - :param suggestion_id: unique id of the suggestion (int):
    - :return db_suggestion: SuggestionResponse object:
    """
    db_suggestion = db.get(schemas.Suggestion, suggestion_id)
    if not db_suggestion or db_suggestion.user_id != user_id:
        raise HTTPException(
            status_code=404,
            detail=f"Suggestion with suggestion_id {suggestion_id} for user with user_id {user_id} not found"
        )

    # Get only SearchCreate Fields, that actually got send within the request
    suggestion_update = suggestion.model_dump(exclude_unset=True)

    # Map through the dictionary to update the database entry
    for key, value in suggestion_update.items():
        setattr(db_suggestion, key, value)

    db.commit()
    db.refresh(db_suggestion)
    return db_suggestion

@router.delete("/users/{user_id}/suggestions/{suggestion_id}",
               response_model=models.SuggestionResponse)
async def delete_suggestion(db: db_dependency,
                            user_id: Annotated[int,Path(
                                description="The unique ID of the user",
                                examples=[40451]
                            )],
                            suggestion_id: Annotated[int, Path(
                                description="The unique ID of the suggestion",
                                examples=[40451]
                            )]
    ):
    """
    - delete suggestion with suggestion_id, from user with user_id and its search history with search_id.
    - :param user_id: unique id of the user (int):
    - :param search_id: unique id of the search (int):
    - :param suggestion_id: unique id of the suggestion (int):
    - :return: SuggestionResponse object:
    """
    db_suggestion = db.get(schemas.Suggestion, suggestion_id)
    if not db_suggestion or db_suggestion.user_id != user_id:
        raise HTTPException(
            status_code=404,
            detail=f"Suggestion with suggestion_id {suggestion_id} for user with user_id {user_id} not found"
        )

    db.delete(db_suggestion)
    db.commit()

    return db_suggestion

# ///////////////// End of Suggestions routes ///////////////// #
# ///////////////// Tripplan specific C.R.U.D. routes ///////////////// #

@router.post("/users/{user_id}/{search_id}/{suggestion_id}/tripplan",
             response_model=models.TripplanResponse,
             status_code=status.HTTP_201_CREATED)
async def create_tripplan(db: db_dependency,
                          user_id: Annotated[int,Path(
                              description="The unique ID of the user",
                              examples=[40451]
                          )],
                          search_id: Annotated[int, Path(
                              description="The unique ID of the search",
                              examples=[40451]
                          )],
                          suggestion_id: Annotated[int, Path(
                              description="The unique ID of the suggestion",
                              examples=[40451]
                          )],
                          tripplan: Annotated[models.TripplanCreate, Body(
                              description="TripplanCreate object."
                          )]
    ):
    """
    - Create a Trip plan entry linked to user with user_id and its search history with search_id
    and resulted suggestion with suggestion_id.
    - :param user_id: unique id of the user (int):
    - :param search_id: unique id of the search (int):
    - :param suggestion_id: unique id of the suggestion (int):
    - :param tripplan: A TripplanCreate object.
    - :return tripplan: TripplanResponse object:
    """
    db_tripplan = schemas.Tripplan(
        title=tripplan.title,
        start_time=tripplan.start_time,
        end_time=tripplan.end_time,
        stopps=tripplan.stopps,
        suggestion_id=suggestion_id,
        search_id=search_id,
        user_id=user_id
    )
    db.add(db_tripplan)
    db.commit()

    return db_tripplan

@router.get("/users/{user_id}/tripplans", response_model=List[models.TripplanResponse])
async def get_tripplans(db: db_dependency,
                        user_id: Annotated[int,Path(
                            description="The unique ID of the user",
                            examples=[40451]
                        )]
    ):
    """
    - Get all Trip plans linked to user with user_id.
    - :param user_id: unique id of the user (int):
    - :return db_tripplans: List of TripplansResponse object/s:
    """
    db_tripplans = db.query(schemas.Tripplan).filter(schemas.Tripplan.user_id == user_id).all()
    if not db_tripplans:
        raise HTTPException(
            status_code=404,
            detail=f"Tripplan(s) from user with user_id {user_id} not found"
        )

    return db_tripplans

@router.get("/users/{user_id}/tripplans/{tripplan_id}", response_model=models.TripplanResponse)
async def get_tripplan(db: db_dependency,
                       user_id: Annotated[int,Path(
                           description="The unique ID of the user",
                           examples=[40451]
                       )],
                       tripplan_id: Annotated[int,Path(
                           description="The unique ID of the tripplan",
                           examples=[40451]
                       )]
    ):
    """
    - Get Trip plan by its ID from user with user_id.
    - :param user_id: unique id of the user (int):
    - :param tripplan_id: unique id of the tripplan (int):
    - :return db_tripplan: TripplanResponse object:
    """
    db_tripplan = db.get(schemas.Tripplan, tripplan_id)
    if not db_tripplan or db_tripplan.user_id != user_id:
        raise HTTPException(
            status_code=404,
            detail=f"Tripplan with id {tripplan_id} from user with user_id {user_id} not found"
        )

    return db_tripplan

@router.put("/users/{user_id}/tripplans/{tripplan_id}", response_model=models.TripplanResponse)
async def update_tripplan(db: db_dependency,
                          user_id: Annotated[int,Path(
                              description="The unique ID of the user",
                              examples=[40451]
                          )],
                          tripplan_id: Annotated[int,Path(
                              description="The unique ID of the tripplan",
                              examples=[40451]
                          )],
                          tripplan: Annotated[models.TripplanCreate, Body(
                              description="TripplanCreate object."
                          )]
    ):
    """
    - Update Tripplan by its ID from user with user_id.
    - :param user_id: unique id of the user (int):
    - :param tripplan_id: unique id of the tripplan (int):
    - :return db_tripplan: TripplanResponse object:
    """
    db_tripplan = db.get(schemas.Tripplan, tripplan_id)
    if not db_tripplan or db_tripplan.user_id != user_id:
        raise HTTPException(
            status_code=404,
            detail=f"Tripplan with id {tripplan_id} from user with user_id {user_id} not found"
        )

    # Get only SearchCreate Fields, that actually got send within the request
    tripplan_update = tripplan.model_dump(exclude_unset=True)

    # Map through the dictionary to update the database entry
    for key, value in tripplan_update.items():
        setattr(db_tripplan, key, value)

    db.commit()
    db.refresh(db_tripplan)
    return db_tripplan

@router.delete("/users/{user_id}/tripplans/{tripplan_id}")
async def delete_tripplan(db: db_dependency,
                          user_id: Annotated[int,Path(
                              description="The unique ID of the user",
                              examples=[40451]
                          )],
                          tripplan_id: Annotated[int,Path(
                              description="The unique ID of the tripplan",
                              examples=[40451]
                          )]
    ):
    """
    - Delete Tripplan by its ID from user with user_id.
    - :param user_id: unique id of the user (int):
    - :param tripplan_id: unique id of the tripplan (int):
    - :return db_tripplan: TripplanResponse object:
    """
    db_tripplan = db.get(schemas.Tripplan, tripplan_id)
    if not db_tripplan or db_tripplan.user_id != user_id:
        raise HTTPException(
            status_code=404,
            detail=f"Tripplan with id {tripplan_id} from user with user_id {user_id} not found"
        )

    db.delete(db_tripplan)
    db.commit()

    return db_tripplan