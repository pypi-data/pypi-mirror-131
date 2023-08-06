from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .language import Language
from ..regions.region import Region


class LanguageTreeNode(MPTTModel):
    """
    Data model representing a region's language tree. Each tree node is a single object instance and the whole tree is
    identified by the root node. The base functionality inherits from the package `django-mptt
    <https://django-mptt.readthedocs.io/en/latest/index.html>`_ (Modified Preorder Tree Traversal).
    """

    language = models.ForeignKey(
        Language,
        on_delete=models.PROTECT,
        related_name="language_tree_nodes",
        verbose_name=_("language"),
    )
    parent = TreeForeignKey(
        "self",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="children",
        verbose_name=_("source language"),
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="language_tree_nodes",
        verbose_name=_("region"),
    )
    visible = models.BooleanField(
        default=True,
        verbose_name=_("visible"),
        help_text=_("Defined if this language should be delivered via the API"),
    )
    active = models.BooleanField(
        default=True,
        verbose_name=_("active"),
        help_text=_("Defined if content in this language can be created or edited"),
    )
    created_date = models.DateTimeField(
        default=timezone.now,
        verbose_name=_("creation date"),
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_("modification date"),
    )

    @property
    def slug(self):
        """
        Returns the slug of this node's language

        :return: The language slug of this language node
        :rtype: str
        """
        return self.language.slug

    @property
    def native_name(self):
        """
        Returns the native name of this node's language

        :return: The native name of this language node
        :rtype: str
        """
        return self.language.native_name

    @property
    def english_name(self):
        """
        Returns the name of this node's language in English

        :return: The English name of this language node
        :rtype: str
        """
        return self.language.english_name

    @property
    def translated_name(self):
        """
        Returns the name of this node's language in the current backend language

        :return: The translated name of this language node
        :rtype: str
        """
        return self.language.translated_name

    @property
    def text_direction(self):
        """
        Returns the text direction (e.g. left-to-right) of this node's language

        :return: The text direction name of this language node
        :rtype: str
        """
        return self.language.text_direction

    @property
    def depth(self):
        """
        Counts how many ancestors the node has. If the node is the root node, its depth is `0`.

        :return: The depth of this language node
        :rtype: str
        """
        return len(self.get_ancestors())

    def __str__(self):
        """
        This overwrites the default Django :meth:`~django.db.models.Model.__str__` method which would return ``LanguageTreeNode object (id)``.
        It is used in the Django admin backend and as label for ModelChoiceFields.

        :return: A readable string representation of the language node
        :rtype: str
        """
        return self.translated_name

    def __repr__(self):
        """
        This overwrites the default Django ``__repr__()`` method which would return ``<LanguageTreeNode: LanguageTreeNode object (id)>``.
        It is used for logging.

        :return: The canonical string representation of the language node
        :rtype: str
        """
        return f"<LanguageTreeNode (id: {self.id}, language: {self.language.slug}, region: {self.region})>"

    class Meta:
        #: The verbose name of the model
        verbose_name = _("language tree node")
        #: The plural verbose name of the model
        verbose_name_plural = _("language tree nodes")
        #: There cannot be two language tree nodes with the same region and language
        unique_together = (
            (
                "language",
                "region",
            ),
        )
        #: The default permissions for this model
        default_permissions = ("change", "delete", "view")
        #: The fields which are used to sort the returned objects of a QuerySet
        ordering = ["region", "level", "parent__pk"]
