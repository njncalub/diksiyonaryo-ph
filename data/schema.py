import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType

from .models import (
    Word as WordModel,
)


class Word(MongoengineObjectType):
    class Meta:
        model = WordModel
        interfaces = (Node,)


class Query(graphene.ObjectType):
    node = Node.Field()
    words = MongoengineConnectionField(Word)
    
    def resolve_words(self, info, entry=None):
        if entry:
            return list(WordModel.objects.filter(entry=entry))
        
        return list(WordModel.objects.all())


schema = graphene.Schema(query=Query, types=[Word])
