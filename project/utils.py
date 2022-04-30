import tmdbv3api
from .models import FilmList


def searchFilms(search: str):
    """Search TMDb Movies

    Args:
        search (str): search title of movie
    """
    return tmdbv3api.Movie().search(search)


def getListById(list_id: int):
    return FilmList.query.filter_by(id=list_id).first()


def buildList(list_id: int):
    """Gets FilmList from DB and combines with TMDb data

    Args:
        list_id (int): _description_
    """
    item = getListById(list_id)
    if item.film_list:
        if item.film_list.find(",") > -1:
            item.film_list = [
                tmdbv3api.Movie().details(i) for i in item.film_list.split(",")
            ]
        else:
            item.film_list = [tmdbv3api.Movie().details(item.film_list)]
    return item


if __name__ == "__maint__":
    film = tmdbv3api.Movie().details(92749)
    print(film)
