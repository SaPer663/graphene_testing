from typing import Optional

from django.db.models.query import QuerySet

import graphene

from graphene_django.types import DjangoObjectType, ObjectType

from movies.models import Actor, Movie


class ActorType(DjangoObjectType):
    class Meta:
        model = Actor


class MovieType(DjangoObjectType):
    class Meta:
        model = Movie


class Query(ObjectType):
    """Получение данных."""
    actor = graphene.Field(ActorType, id=graphene.Int())
    movie = graphene.Field(MovieType, id=graphene.Int())
    actors = graphene.List(ActorType)
    movies = graphene.List(MovieType)

    def resolve_actor(self, info, **kwargs) -> Optional[Actor]:
        id = kwargs.get('id')
        if id is not None:
            return Actor.objects.get(id=id)

    def resolve_movie(self, info, **kwargs) -> Optional[Movie]:
        id = kwargs.get('id')
        if id is not None:
            return Movie.objects.get(id=id)

    def resolve_actors(self, info, **kwargs) -> QuerySet:
        return Actor.objects.all()

    def resolve_movies(self, info, **kwargs) -> QuerySet:
        return Movie.objects.all()


class ActorInput(graphene.InputObjectType):
    """Объект изменения данных Актёра."""
    id = graphene.ID()
    name = graphene.String()


class MovieInput(graphene.InputObjectType):
    """Объект изменения данных Фильма."""
    id = graphene.ID()
    title = graphene.String()
    actors = graphene.List(ActorInput)
    year = graphene.Int()


class CreateActor(graphene.Mutation):
    """Добавление записи о актёре в базу."""
    class Arguments:
        input_object = ActorInput(required=True)
    ok = graphene.Boolean()
    actor = graphene.Field(ActorType())

    @staticmethod
    def mutate(root, info, input_object: Actor = None):
        actor, _ = Actor.objects.get_or_create(name=input_object.name)
        return CreateActor(ok=True, actor=actor)


class UpdateActor(graphene.Mutation):
    """Обновление данных об актёре."""
    class Arguments:
        id = graphene.Int(required=True)
        input_object = ActorInput(required=True)

    ok = graphene.Boolean()
    actor = graphene.Field(ActorType)

    @staticmethod
    def mutate(root, info, id, input_object: Actor = None):
        ok = False
        actor = Actor.objects.get(id=id)
        if not actor:
            return UpdateActor(ok=ok, actor=None)
        ok = True
        actor.name = input_object.name
        actor.save()
        return UpdateActor(ok=ok, actor=actor)


class CreateMovie(graphene.Mutation):
    """Создаёт запись в базе о фильме."""
    class Arguments:
        input_object = MovieInput(required=True)

    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, input_object: Movie = None):
        ok = True
        actors = []
        for input_actor in input_object.actors:
            actor = Actor.objects.get(id=input_actor.id)
            if actor is None:
                return CreateMovie(ok=False, movie=None)
            actors.append(actor)
        movie, _ = Movie.objects.get_or_create(
            title=input_object.title,
            year=input_object.year
        )
        movie.actors.set(actors)
        return CreateMovie(ok=ok, movie=movie)


class UpdateMovie(graphene.Mutation):
    """Обновляет информацию о фильме."""
    class Arguments:
        id = graphene.Int(required=True)
        input_object = MovieInput(required=True)

    ok = graphene.Boolean()
    movie = graphene.Field(MovieType)

    @staticmethod
    def mutate(root, info, id, input_object: Movie = None):
        ok = False
        movie = Movie.objects.get(id=id)
        if not movie:
            return UpdateMovie(ok=ok, movie=None)
        actors = []
        for input_actor in input_object.actors:
            actor = Actor.objects.get(id=input_actor.id)
            if actor is None:
                return UpdateMovie(ok=ok, movie=None)
            actors.append(actor)
        ok = True
        movie.title = input_object.title
        movie.year = input_object.year
        movie.actors.set(actors)
        movie.save()
        return UpdateMovie(ok=ok, movie=movie)


class Mutation(graphene.ObjectType):
    """Изменения данных."""
    create_actor = CreateActor.Field()
    update_actor = UpdateActor.Field()
    create_movie = CreateMovie.Field()
    update_movie = UpdateMovie.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
