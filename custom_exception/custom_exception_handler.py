from rest_framework.views import exception_handler
from rest_framework.response import Response


def custom_handler(exc, context):
    """
        This function helps see the
        errors that might occur in the
        project and easily track it.
    """
    response = exception_handler(exc, context)
    # if the exc is an exception, response won't return anything

    if response is not None:
        # i.e it is not an exception
        return response

    print(exc, context, "Trace")
    exc_list = str(exc).split("DETAIL: ")
    print(str(exc))

    return Response({"error": exc_list[-1]}, status="403")
