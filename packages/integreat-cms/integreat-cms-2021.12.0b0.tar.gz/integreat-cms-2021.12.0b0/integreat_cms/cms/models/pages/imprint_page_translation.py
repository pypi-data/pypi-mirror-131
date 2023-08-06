import logging

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .abstract_base_page_translation import AbstractBasePageTranslation
from .imprint_page import ImprintPage
from ..languages.language import Language


logger = logging.getLogger(__name__)


class ImprintPageTranslation(AbstractBasePageTranslation):
    """
    Data model representing a imprint translation
    """

    page = models.ForeignKey(
        ImprintPage,
        on_delete=models.CASCADE,
        related_name="translations",
        verbose_name=_("imprint"),
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name="imprint_translations",
        verbose_name=_("language"),
    )
    title = models.CharField(
        max_length=1024,
        verbose_name=_("title of the imprint"),
    )
    text = models.TextField(
        blank=True,
        verbose_name=_("content of the imprint"),
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="imprint_translations",
        verbose_name=_("creator"),
    )

    @property
    def permalink(self):
        """
        This property calculates the permalink dynamically

        :return: The permalink of the imprint
        :rtype: str
        """
        return "/".join(
            filter(
                None,
                [self.page.region.slug, self.language.slug, settings.IMPRINT_SLUG],
            )
        )

    @property
    def base_link(self):
        """
        This property calculates the absolute imprint link without the slug dynamically

        :return: The base link of the page
        :rtype: str
        """
        return (
            "/".join(
                [
                    settings.WEBAPP_URL,
                    self.page.region.slug,
                    self.language.slug,
                ]
            )
            + "/"
        )

    @property
    def short_url(self):
        """
        This function returns the absolute short url to the imprint translation

        :return: The short url of an imprint translation
        :rtype: str
        """

        return settings.BASE_URL + reverse(
            "expand_imprint_translation_id", kwargs={"imprint_translation_id": self.id}
        )

    @property
    def slug(self):
        """
        For compatibility with the other page translations, a slug property is useful.

        :return: pseudo slug for the imprint translation
        :rtype: str
        """
        return settings.IMPRINT_SLUG

    class Meta:
        #: The verbose name of the model
        verbose_name = _("imprint translation")
        #: The plural verbose name of the model
        verbose_name_plural = _("imprint translations")
        #: The fields which are used to sort the returned objects of a QuerySet
        ordering = ["page", "-version"]
        #: The default permissions for this model
        default_permissions = ()
