from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ValidationError

from api.base.renderers import JSONAPIRenderer
from api.base.exceptions import JSONAPIException

class JSONAPIParser(JSONParser):
    """
    Parses JSON-serialized data. Overrides media_type.
    """
    media_type = 'application/vnd.api+json'
    renderer_class = JSONAPIRenderer

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as JSON and returns the resulting data
        """
        result = super(JSONAPIParser, self).parse(stream, media_type=media_type, parser_context=parser_context)
        if not isinstance(result, dict):
            raise ValidationError("Invalid data. Expected a dictionary but got {}".format(type(result)))
        data = result.get('data', {})

        if data:
            if 'attributes' not in data:
                raise JSONAPIException(source={'pointer': '/data/attributes'}, detail='This field is required.')
            id = data.get('id')
            object_type = data.get('type')
            attributes = data.get('attributes')

            parsed = {'id': id, 'type': object_type}
            parsed.update(attributes)

            return parsed

        else:
            raise JSONAPIException(source={'pointer': '/data'}, detail='This field is required.')


class JSONAPIParserForRegularJSON(JSONAPIParser):
    media_type = 'application/json'
