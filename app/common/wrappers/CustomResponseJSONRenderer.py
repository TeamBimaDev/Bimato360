from rest_framework.renderers import JSONRenderer


class CustomResponseJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
            'succeeded': True,
            "code": status_code,
            "data": data,
            "message": None
        }
        if not str(status_code).startswith('2'):
            response["status"] = "error"
            response["data"] = None
            response["code"] = status_code
            try:
                response["message"] = data["detail"]
            except KeyError:
                response["data"] = data

        return super(CustomResponseJSONRenderer, self).render(response, accepted_media_type, renderer_context)
