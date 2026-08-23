from abc import ABC, abstractmethod

from django.db.models import Q


class Specification(ABC):
    """Define the base interface for specifications.

    Specifications can be combined using logical operators and translated into
    Django `Q` objects for queryset filtering.
    """

    @abstractmethod
    def is_satisfied_by(self, candidate):
        """Check whether a candidate satisfies the specification.

        Args:
            candidate (Any): Candidate object to evaluate.

        Returns:
            bool: True when the candidate satisfies the specification.
        """
        pass

    @abstractmethod
    def as_q(self) -> Q:
        """Return a Django Q object representing the specification.

        Returns:
            Q: Django Q object for queryset filtering.
        """
        pass

    # Logical operators are defined here.
    def __and__(self, other) -> "AndSpecification":
        """Combine this specification with another using logical AND.

        Args:
            other (Specification): Specification to combine.

        Returns:
            AndSpecification: Combined specification.
        """
        return AndSpecification(self, other)

    def __or__(self, other) -> "OrSpecification":
        """Combine this specification with another using logical OR.

        Args:
            other (Specification): Specification to combine.

        Returns:
            OrSpecification: Combined specification.
        """
        return OrSpecification(self, other)

    def __invert__(self) -> "NotSpecification":
        """Negate this specification.

        Returns:
            NotSpecification: Negated specification.
        """
        return NotSpecification(self)

    def filter(self, queryset):
        """Filter a queryset using this specification.

        Args:
            queryset (QuerySet): Queryset to filter.

        Returns:
            QuerySet: Filtered queryset.
        """
        return queryset.filter(self.as_q())

    def flatten(self):
        """Return all simple specifications in the chain.

        Returns:
            list[Specification]: Flattened list of specifications.
        """
        return [self]


class AndSpecification(Specification):
    """Combine two specifications with logical AND."""

    def __init__(self, left: Specification, right: Specification):
        self.left = left
        self.right = right

    def is_satisfied_by(self, candidate):
        """Check whether the candidate satisfies both specifications.

        Args:
            candidate (Any): Candidate object to evaluate.

        Returns:
            bool: True when both specifications are satisfied.
        """
        return self.left.is_satisfied_by(candidate) and self.right.is_satisfied_by(candidate)

    def as_q(self):
        """Return a combined Q object using logical AND.

        Returns:
            Q: Combined Q object.
        """
        return self.left.as_q() & self.right.as_q()

    def flatten(self):
        """Return a flattened list of contained specifications.

        Returns:
            list[Specification]: Flattened list of specifications.
        """
        return self.left.flatten() + self.right.flatten()


class OrSpecification(Specification):
    """Combine two specifications with logical OR."""

    def __init__(self, left: Specification, right: Specification):
        self.left = left
        self.right = right

    def is_satisfied_by(self, candidate):
        """Check whether the candidate satisfies either specification.

        Args:
            candidate (Any): Candidate object to evaluate.

        Returns:
            bool: True when at least one specification is satisfied.
        """
        return self.left.is_satisfied_by(candidate) or self.right.is_satisfied_by(candidate)

    def as_q(self):
        """Return a combined Q object using logical OR.

        Returns:
            Q: Combined Q object.
        """
        return self.left.as_q() | self.right.as_q()

    def flatten(self):
        """Return a flattened list of contained specifications.

        Returns:
            list[Specification]: Flattened list of specifications.
        """
        return self.left.flatten() + self.right.flatten()


class NotSpecification(Specification):
    """Negate a specification."""

    def __init__(self, spec: Specification):
        self.spec = spec

    def is_satisfied_by(self, candidate):
        """Check whether the candidate does not satisfy the specification.

        Args:
            candidate (Any): Candidate object to evaluate.

        Returns:
            bool: True when the specification is not satisfied.
        """
        return not self.spec.is_satisfied_by(candidate)

    def as_q(self):
        """Return a negated Q object.

        Returns:
            Q: Negated Q object.
        """
        return ~self.spec.as_q()

    def flatten(self):
        """Return a flattened list including the inner specification.

        Returns:
            list[Specification]: Flattened list of specifications.
        """
        return self.spec.flatten() + [self]
