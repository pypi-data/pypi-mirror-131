import logging

from html import escape

from django.conf import settings
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from .abstract_base_page import AbstractBasePage
from ..languages.language import Language
from ..regions.region import Region
from ..media.media_file import MediaFile
from ..users.organization import Organization
from ...utils.translation_utils import ugettext_many_lazy as __

logger = logging.getLogger(__name__)


class Page(MPTTModel, AbstractBasePage):
    """
    Data model representing a page.
    """

    parent = TreeForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="children",
        verbose_name=_("parent page"),
    )
    icon = models.ForeignKey(
        MediaFile,
        verbose_name=_("icon"),
        on_delete=models.SET_NULL,
        related_name="icon_pages",
        blank=True,
        null=True,
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="pages",
        verbose_name=_("region"),
    )
    mirrored_page = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="mirroring_pages",
        verbose_name=_("mirrored page"),
        help_text=_(
            "If the page embeds live content from another page, it is referenced here."
        ),
    )
    mirrored_page_first = models.BooleanField(
        default=True,
        null=True,
        blank=True,
        verbose_name=_("Position of mirrored page"),
        help_text=_(
            "If a mirrored page is set, this field determines whether the live content is embedded before the content of this page or after."
        ),
    )
    editors = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="editable_pages",
        verbose_name=_("editors"),
        help_text=__(
            _("A list of users who have the permission to edit this specific page."),
            _(
                "Only has effect if these users do not have the permission to edit pages anyway."
            ),
        ),
    )
    publishers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="publishable_pages",
        verbose_name=_("publishers"),
        help_text=__(
            _("A list of users who have the permission to publish this specific page."),
            _(
                "Only has effect if these users do not have the permission to publish pages anyway."
            ),
        ),
    )
    organization = models.ForeignKey(
        Organization,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pages",
        verbose_name=_("responsible organization"),
        help_text=_(
            "This allows all members of the organization to edit and publish this page."
        ),
    )

    @property
    def explicitly_archived_ancestors(self):
        """
        This returns all of the page's ancestors which are archived.

        :return: The QuerySet of archived ancestors
        :rtype: ~mptt.querysets.TreeQuerySet [ ~integreat_cms.cms.models.pages.page.Page ]
        """
        return self.get_ancestors().filter(explicitly_archived=True)

    @property
    def implicitly_archived(self):
        """
        This checks whether one of the page's ancestors is archived which means that this page is implicitly archived as well.

        :return: Whether or not this page is implicitly archived
        :rtype: bool
        """
        return self.explicitly_archived_ancestors.exists()

    @property
    def archived(self):
        """
        A hierarchical page is archived either explicitly if ``explicitly_archived=True`` or implicitly if one of its
        ancestors is explicitly archived.

        :return: Whether or not this page is archived
        :rtype: bool
        """
        return self.explicitly_archived or self.implicitly_archived

    @property
    def languages(self):
        """
        This property returns a list of all :class:`~integreat_cms.cms.models.languages.language.Language` objects, to which a page
        translation exists.

        :return: list of all :class:`~integreat_cms.cms.models.languages.language.Language` a page is translated into
        :rtype: list [ ~integreat_cms.cms.models.languages.language.Language ]
        """
        return Language.objects.filter(page_translations__page=self)

    @property
    def depth(self):
        """
        Counts how many ancestors the page has. If the page is the root page, its depth is `0`.

        :return: The depth of this page in its page tree
        :rtype: str
        """
        return len(self.get_ancestors())

    @classmethod
    def get_root_pages(cls, region_slug):
        """
        Gets all root pages

        :param region_slug: Slug defining the region
        :type region_slug: str

        :return: All root pages i.e. pages without parents
        :rtype: ~mptt.querysets.TreeQuerySet [ ~integreat_cms.cms.models.pages.page.Page ]
        """
        return Page.objects.filter(region__slug=region_slug, parent=None)

    def get_previous_sibling(self, *filter_args, **filter_kwargs):
        r"""
        This function gets all previous siblings of a page

        :param \*filter_args: The supplied arguments
        :type \*filter_args: list

        :param \**filter_kwargs: The supplied kwargs
        :type \**filter_kwargs: list

        :return: The previous sibling
        :rtype: ~integreat_cms.cms.models.pages.page.Page
        """
        # Only consider siblings from this region
        filter_kwargs["region"] = self.region
        return super().get_previous_sibling(*filter_args, **filter_kwargs)

    def get_next_sibling(self, *filter_args, **filter_kwargs):
        r"""
        This function gets the next sibling of a page

        :param \*filter_args: The supplied arguments
        :type \*filter_args: list

        :param \**filter_kwargs: The supplied kwargs
        :type \**filter_kwargs: list

        :return: The next sibling
        :rtype: ~integreat_cms.cms.models.pages.page.Page
        """
        # Only consider siblings from this region
        filter_kwargs["region"] = self.region
        return super().get_next_sibling(*filter_args, **filter_kwargs)

    def get_siblings(self, include_self=False):
        """
        This function gets all siblings of a page

        :param include_self: gives state of include_self
        :type include_self: bool

        :return: All siblings of this page
        :rtype: ~django.db.models.query.QuerySet [ ~integreat_cms.cms.models.pages.page.Page ]
        """
        # Return only siblings from the same region
        return (
            super().get_siblings(include_self=include_self).filter(region=self.region)
        )

    def get_descendants_max_depth(self, include_self, max_depth):
        """
        Return all descendants with depth less or equal to max depth relative to this nodes depth

        :param include_self: Whether to include this node in the result
        :type include_self: bool

        :param max_depth: The nodes maximum depth in the tree
        :type max_depth: int

        :return: All descendants of this node with relative max depth
        :rtype: ~mptt.querysets.TreeQuerySet [ ~integreat_cms.cms.models.pages.page.Page ]
        """
        return (
            super()
            .get_descendants(include_self=include_self)
            .filter(level__lte=self.get_level() + max_depth)
        )

    def get_mirrored_page_translation(self, language_slug):
        """
        Mirrored content always includes the live content from another page. This content needs to be added when
        delivering content to end users.

        :param language_slug: The slug of the requested :class:`~integreat_cms.cms.models.languages.language.Language`
        :type language_slug: str

        :return: The content of a mirrored page
        :rtype: str
        """
        if self.mirrored_page:
            return self.mirrored_page.get_public_translation(language_slug)
        return None

    def __str__(self):
        """
        This overwrites the default Django :meth:`~django.db.models.Model.__str__` method which would return ``Page object (id)``.
        It is used in the Django admin backend and as label for ModelChoiceFields.

        :return: A readable string representation of the page
        :rtype: str
        """
        label = " &rarr; ".join(
            [
                # escape page title because string is marked as safe afterwards
                escape(ancestor.best_translation.title)
                for ancestor in self.get_ancestors(include_self=True)
            ]
        )
        # Add warning if page is archived
        if self.archived:
            label += " (&#9888; " + _("Archived") + ")"
        # mark as safe so that the arrow and the warning triangle are not escaped
        return mark_safe(label)

    class Meta:
        #: The verbose name of the model
        verbose_name = _("page")
        #: The plural verbose name of the model
        verbose_name_plural = _("pages")
        #: The default permissions for this model
        default_permissions = ("change", "delete", "view")
        #: The custom permissions for this model
        permissions = (
            ("publish_page", "Can publish page"),
            ("grant_page_permissions", "Can grant page permission"),
        )
