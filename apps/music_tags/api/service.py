from http import HTTPStatus

from ninja.responses import Status

from apps.comun.api.service import GenericModelService


class MusicTagsService(GenericModelService):  # noqa
    def get_all(self, **kwargs):  # noqa
        qs = super().get_all(**kwargs)
        return qs.order_by("tag")

    def get_random_music_tag(self):
        """In real scenarios there shouldn't exist an endpoint that fetches random resources.

        Unless it is explicitly required.
        """
        music_tag = self.model.objects.order_by("?").first()
        if not music_tag:
            return Status(HTTPStatus.NOT_FOUND, None)

        return Status(HTTPStatus.OK, music_tag)
