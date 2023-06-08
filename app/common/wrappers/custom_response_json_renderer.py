from rest_framework.renderers import JSONRenderer


class CustomResponseJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        if 'succeeded' not in data:
            response = {
                'succeeded': True,
                "code": status_code,
                "data": data,
                "message": None
            }
            if not str(status_code).startswith('2'):
                response["succeeded"] = False
                response["status"] = "error"
                response["data"] = None
                response["code"] = status_code
                try:
                    response["message"] = data["detail"]
                except KeyError:
                    response["data"] = data
            data = response

        return super(CustomResponseJSONRenderer, self). \
            render(data, accepted_media_type, renderer_context)
