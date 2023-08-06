"""Django Object Model Utilities."""


from __future__ import annotations

from abc import abstractmethod
from sys import version_info
from typing import Union
from typing import List   # Py3.9+: use generic types
from uuid import UUID, uuid4

from django.db.models.base import Model
from django.db.models.constraints import BaseConstraint
from django.db.models.fields import (AutoField, BigAutoField, SmallAutoField,
                                     UUIDField,
                                     CharField,
                                     DateField)
from django.db.models.indexes import Index
from django.utils.functional import classproperty

from django.db.models.manager import Manager

from model_utils.models import TimeStampedModel

from .str import MAX_CHAR_FLD_LEN

if version_info >= (3, 9):
    from collections.abc import Sequence
else:
    from typing import Sequence   # pylint: disable=ungrouped-imports


__all__: Sequence[str] = (
    'PGSQL_IDENTIFIER_MAX_LEN',
    '_ModelWithObjectsManagerAndDefaultMetaOptionsABC',
    '_ModelWithIntPKABC', '_ModelWithBigIntPKABC', '_ModelWithSmallIntPKABC',
    '_ModelWithUUIDPKABC',
    '_ModelWithNullableDateABC', '_ModelWithNonNullableDateABC',
    '_ModelWithAutoCompleteSearchFieldsABC',
    '_ModelWithUUIDPKAndOptionalUniqueNameAndTimestampsABC',
)


# postgresql.org/docs/devel/sql-syntax-lexical.html#SQL-SYNTAX-IDENTIFIERS
PGSQL_IDENTIFIER_MAX_LEN = 63


# Field options:
# docs.djangoproject.com/en/dev/ref/models/fields/#common-model-field-options

# - null:
#   docs.djangoproject.com/en/dev/ref/models/fields/#null

# - blank:
#   docs.djangoproject.com/en/dev/ref/models/fields/#blank

# - choices:
#   docs.djangoproject.com/en/dev/ref/models/fields/#choices
#   - Enumeration types:
#     docs.djangoproject.com/en/dev/ref/models/fields/#enumeration-types

# - db_column:
#   docs.djangoproject.com/en/dev/ref/models/fields/#db-column

# - db_index:
#   docs.djangoproject.com/en/dev/ref/models/fields/#db-index

# - db_tablespace:
#   docs.djangoproject.com/en/dev/ref/models/fields/#db-tablespace

# - default:
#   docs.djangoproject.com/en/dev/ref/models/fields/#default

# - editable:
#   docs.djangoproject.com/en/dev/ref/models/fields/#editable

# - error_messages:
#   docs.djangoproject.com/en/dev/ref/models/fields/#error-messages

# - help_text:
#   docs.djangoproject.com/en/dev/ref/models/fields/#help-text

# - primary_key:
#   docs.djangoproject.com/en/dev/ref/models/fields/#primary-key

# - unique:
#   docs.djangoproject.com/en/dev/ref/models/fields/#unique

# - unique_for_date:
#   docs.djangoproject.com/en/dev/ref/models/fields/#unique-for-date

# - unique_for_month:
#   docs.djangoproject.com/en/dev/ref/models/fields/#unique-for-month

# - unique_for_year:
#   docs.djangoproject.com/en/dev/ref/models/fields/#unique-for-year

# - verbose_name:
#   docs.djangoproject.com/en/dev/ref/models/fields/#verbose-name

# - validators:
#   docs.djangoproject.com/en/dev/ref/models/fields/#validators


# Model attribute interpolation:
# - app_label: e.g., 'App_Label'
# - class: cls.__name__.lower(), e.g., 'modelclass'
# - model_name: cls._meta.model_name.lower(), e.g., 'modelclass'
# - object_name: e.g., 'ModelClass'


class _ModelWithObjectsManagerAndDefaultMetaOptionsABC(Model):
    # docs.djangoproject.com/en/dev/ref/models/class/#objects
    objects: Manager = Manager()

    # docs.djangoproject.com/en/dev/ref/models/options/#model-meta-options
    class Meta:   # pylint: disable=too-few-public-methods
        """Metadata."""

        # docs.djangoproject.com/en/dev/ref/models/options/#abstract
        abstract: bool = True

        # docs.djangoproject.com/en/dev/ref/models/options/#app-label
        # app_label: str = '...'

        # docs.djangoproject.com/en/dev/ref/models/options/#base-manager-name
        base_manager_name: str = 'objects'

        # docs.djangoproject.com/en/dev/ref/models/options/#db-table
        # docs.djangoproject.com/en/dev/ref/models/options/#table-names
        # db_table: str = '...'

        # docs.djangoproject.com/en/dev/ref/models/options/#db-tablespace
        db_tablespace: str = ''

        # docs.djangoproject.com/en/dev/ref/models/options/#default-manager-name
        default_manager_name: str = 'objects'

        # docs.djangoproject.com/en/dev/ref/models/options/#default-related-name
        # default_related_name: str = '...'

        # docs.djangoproject.com/en/dev/ref/models/options/#get-latest-by
        # get_latest_by: Union[str, Sequence[str]] = ...

        # docs.djangoproject.com/en/dev/ref/models/options/#managed
        managed: bool = True

        # docs.djangoproject.com/en/dev/ref/models/options/#order-with-respect-to
        # order_with_respect_to: str = '...'

        # docs.djangoproject.com/en/dev/ref/models/options/#ordering
        ordering: Sequence[str] = ()

        # docs.djangoproject.com/en/dev/ref/models/options/#permissions
        permissions: Sequence[tuple[str, str]] = ()

        # docs.djangoproject.com/en/dev/ref/models/options/#default-permissions
        default_permissions: Sequence[str] = 'add', 'change', 'delete', 'view'

        # docs.djangoproject.com/en/dev/ref/models/options/#proxy
        proxy: bool = False

        # docs.djangoproject.com/en/dev/ref/models/options/#required-db-features
        required_db_features: Sequence[str] = ()

        # docs.djangoproject.com/en/dev/ref/models/options/#required-db-vendor
        # required_db_vendor: str = '...'

        # docs.djangoproject.com/en/dev/ref/models/options/#select-on-save
        select_on_save: bool = False

        # docs.djangoproject.com/en/dev/ref/models/options/#indexes
        indexes: Sequence[Index] = ()

        # DEPRECATED
        # docs.djangoproject.com/en/dev/ref/models/options/#unique-together
        # unique_together: Sequence[Union[str, Sequence[str]]] = ()

        # DEPRECATED
        # docs.djangoproject.com/en/dev/ref/models/options/#index-together
        # index_together: Sequence[Union[str, Sequence[str]]] = ()

        # docs.djangoproject.com/en/dev/ref/models/options/#constraints
        constraints: Sequence[BaseConstraint] = ()

        # docs.djangoproject.com/en/dev/ref/models/options/#verbose-name
        # verbose_name: str = '...'

        # docs.djangoproject.com/en/dev/ref/models/options/#verbose-name-plural
        # verbose_name_plural: str  = '...'


class _ModelWithIntPKABC(_ModelWithObjectsManagerAndDefaultMetaOptionsABC):
    # docs.djangoproject.com/en/dev/topics/db/models/#automatic-primary-key-fields
    # docs.djangoproject.com/en/dev/ref/models/fields/#autofield
    id: AutoField = \
        AutoField(
            verbose_name='Integer Primary Key',
            help_text='Integer Primary Key',

            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=False,
            # error_messages={},
            primary_key=True,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            # validators=()
        )

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsABC.Meta):
        # pylint: disable=too-few-public-methods
        """Metadata."""

        abstract = True


class _ModelWithBigIntPKABC(_ModelWithObjectsManagerAndDefaultMetaOptionsABC):
    # docs.djangoproject.com/en/dev/ref/models/fields/#bigautofield
    id: BigAutoField = \
        BigAutoField(
            verbose_name='Big Integer Primary Key',
            help_text='Big Integer Primary Key',

            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=False,
            # error_messages={},
            primary_key=True,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            # validators=()
        )

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsABC.Meta):
        # pylint: disable=too-few-public-methods
        """Metadata."""

        abstract = True


class _ModelWithSmallIntPKABC(
        _ModelWithObjectsManagerAndDefaultMetaOptionsABC):
    # docs.djangoproject.com/en/dev/ref/models/fields/#smallautofield
    id: SmallAutoField = \
        SmallAutoField(
            verbose_name='Small Integer Primary Key',
            help_text='Small Integer Primary Key',

            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=False,
            # error_messages={},
            primary_key=True,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            # validators=()
        )

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsABC.Meta):
        # pylint: disable=too-few-public-methods
        """Metadata."""

        abstract = True


class _ModelWithUUIDPKABC(_ModelWithObjectsManagerAndDefaultMetaOptionsABC):
    uuid: UUIDField = \
        UUIDField(
            verbose_name='UUID',
            help_text='UUID',

            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=uuid4,
            editable=False,
            # error_messages={},
            primary_key=True,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            # validators=()
        )

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsABC.Meta):
        # pylint: disable=too-few-public-methods
        """Metadata."""

        abstract = True

    def __str__(self) -> str:
        return f'{type(self).__name__} #{self.uuid}'


class _ModelWithNullableDateABC(
        _ModelWithObjectsManagerAndDefaultMetaOptionsABC):
    # docs.djangoproject.com/en/dev/ref/models/fields/#datefield
    date: DateField = \
        DateField(
            verbose_name='Date',
            help_text='Date',

            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            # validators=(),

            auto_now_add=False,
            auto_now=False)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsABC.Meta):
        # pylint: disable=too-few-public-methods
        """Metadata."""

        abstract = True


class _ModelWithNonNullableDateABC(
        _ModelWithObjectsManagerAndDefaultMetaOptionsABC):
    # docs.djangoproject.com/en/dev/ref/models/fields/#datefield
    date: DateField = \
        DateField(
            verbose_name='Date',
            help_text='Date',

            null=False,
            blank=False,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            primary_key=False,
            unique=False,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            # validators=(),

            auto_now_add=False,
            auto_now=False)

    class Meta(_ModelWithObjectsManagerAndDefaultMetaOptionsABC.Meta):
        # pylint: disable=too-few-public-methods
        """Metadata."""

        abstract = True


class _ModelWithAutoCompleteSearchFieldsABC:
    @staticmethod
    @abstractmethod
    def search_fields() -> Sequence[str]:
        """Search fields."""
        raise NotImplementedError

    @classmethod
    def autocomplete_search_fields(cls) -> Sequence[str]:
        """Auto-complete search fields."""
        return [f'{search_field}__icontains'
                for search_field in cls.search_fields()]


class _ModelWithUUIDPKAndOptionalUniqueNameAndTimestampsABC(
        _ModelWithUUIDPKABC, TimeStampedModel):
    name: CharField = \
        CharField(
            verbose_name='(optional) Unique Name',
            help_text='(optional) Unique Name',

            max_length=MAX_CHAR_FLD_LEN,

            null=True,
            blank=True,
            choices=None,
            db_column=None,
            db_index=True,
            db_tablespace=None,
            default=None,
            editable=True,
            # error_messages={},
            primary_key=False,
            unique=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            # validators=()
        )

    class Meta(_ModelWithUUIDPKABC.Meta):
        # pylint: disable=too-few-public-methods
        """Metadata."""

        abstract: bool = True

        get_latest_by: Union[str, Sequence[str]] = 'modified'

        ordering: Sequence[str] = 'name', '-modified'

    def __str__(self) -> str:
        return (f'{type(self).__name__} "{self.name}"'
                if self.name
                else super().__str__())

    @property
    def name_or_uuid(self) -> str:
        """Object's Name (if applicable) or UUID."""
        return self.name if self.name else self.uuid

    @classproperty
    def names_or_uuids(cls) -> List[str]:   # noqa: N805
        # pylint: disable=no-self-argument
        """Class's Objects' Names (where applicable) or UUIDs."""
        return [(name if name else uuid)
                for name, uuid in cls.objects.values_list('name', 'uuid')]

    @classmethod
    def get_by_name_or_uuid(cls, name_or_uuid: str) \
            -> _ModelWithUUIDPKAndOptionalUniqueNameAndTimestampsABC:
        """Get Object by Name (if applicable) or UUID."""
        try:   # try looking up object by UUID
            _uuid: UUID = UUID(hex=name_or_uuid, version=4)
            return cls.objects.get(uuid=_uuid)

        except ValueError:
            # else look up by Name
            return cls.objects.get(name=name_or_uuid)
