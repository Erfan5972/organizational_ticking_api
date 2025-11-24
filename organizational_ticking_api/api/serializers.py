from rest_framework import serializers


class PaginatedSwaggerSerializer(serializers.Serializer):
    count = serializers.IntegerField(help_text="Total number of items.")
    next = serializers.CharField(
        allow_null=True, help_text="URL to the next page of results.", required=False
    )
    previous = serializers.CharField(
        allow_null=True,
        help_text="URL to the previous page of results.",
        required=False,
    )
    page_size = serializers.IntegerField(help_text="Number of items per page.")
    results = serializers.ListField(
        child=serializers.DictField(), help_text="List of objects."
    )
    messages = serializers.CharField(help_text="message")


class PaginationParametersSerializer(serializers.Serializer):
    """
    Serializer for pagination parameters.
    """

    p = serializers.IntegerField(required=False, help_text="Requested page number")
    page_size = serializers.IntegerField(
        required=False, help_text="Number of objects per page"
    )
    all = serializers.BooleanField(required=False, help_text="Show all objects")
