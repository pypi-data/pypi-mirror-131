from .abstract_manifold_model_attributes import AbstractManifoldModelAttributes


class LinearAttributes(AbstractManifoldModelAttributes):
    """
    Attributes of leaspy linear models.

    Contains the common attributes & methods to update the linear model's attributes.

    Parameters
    ----------
    name : str
    dimension : int
    source_dimension : int

    Attributes
    ----------
    name : str (default 'linear')
        Name of the associated leaspy model.
    dimension : int
    source_dimension : int
    univariate : bool
        Whether model is univariate or not (i.e. dimension == 1)
    has_sources : bool
        Whether model has sources or not (not univariate and source_dimension >= 1)
    update_possibilities : tuple [str] (default ('all', 'g', 'v0', 'betas') )
        Contains the available parameters to update. Different models have different parameters.
    positions : :class:`torch.Tensor` [dimension] (default None)
        positions = realizations['g'] such that "p0" = positions
    velocities : :class:`torch.Tensor` [dimension] (default None)
        Always positive: exp(realizations['v0'])
    orthonormal_basis : :class:`torch.Tensor` [dimension, dimension - 1] (default None)
    betas : :class:`torch.Tensor` [dimension - 1, source_dimension] (default None)
    mixing_matrix : :class:`torch.Tensor` [dimension, source_dimension] (default None)
        Matrix A such that w_i = A * s_i.

    See Also
    --------
    :class:`~leaspy.models.univariate_model.UnivariateModel`
    :class:`~leaspy.models.multivariate_model.MultivariateModel`
    """

    def __init__(self, name, dimension, source_dimension):

        super().__init__(name, dimension, source_dimension)


    def update(self, names_of_changed_values, values):
        """
        Update model group average parameter(s).

        Parameters
        ----------
        names_of_changed_values : list [str]
            Elements of list must be either:
                * ``all`` (update everything)
                * ``g`` correspond to the attribute :attr:`positions`.
                * ``v0`` (``xi_mean`` if univariate) correspond to the attribute :attr:`velocities`.
                * ``betas`` correspond to the linear combinaison of columns from the orthonormal basis so
                  to derive the :attr:`mixing_matrix`.
        values : dict [str, `torch.Tensor`]
            New values used to update the model's group average parameters

        Raises
        ------
        :exc:`.LeaspyModelInputError`
            If `names_of_changed_values` contains unknown parameters.
        """
        self._check_names(names_of_changed_values)

        compute_betas = False
        compute_positions = False
        compute_velocities = False

        if 'all' in names_of_changed_values:
            names_of_changed_values = self.update_possibilities  # make all possible updates
        if 'betas' in names_of_changed_values:
            compute_betas = True
        if 'g' in names_of_changed_values:
            compute_positions = True
        if ('v0' in names_of_changed_values) or ('xi_mean' in names_of_changed_values):
            compute_velocities = True

        if compute_betas:
            self._compute_betas(values)
        if compute_positions:
            self._compute_positions(values)
        if compute_velocities:
            self._compute_velocities(values)

        if self.has_sources:
            if compute_velocities:
                self._compute_orthonormal_basis()
            if compute_velocities or compute_betas:
                self._compute_mixing_matrix()

    def _compute_positions(self, values):
        """
        Update the attribute ``positions``.

        Parameters
        ----------
        values : dict [str, `torch.Tensor`]
        """
        self.positions = values['g'].clone()


    def _compute_orthonormal_basis(self):
        """
        Compute the attribute ``orthonormal_basis`` which is an orthonormal basis, w.r.t the canonical inner product,
        of the sub-space orthogonal, w.r.t the inner product implied by the metric, to the time-derivative of the geodesic at initial time.
        In linear case, this inner product corresponds to canonical Euclidean one.
        """
        if not self.has_sources:
            return

        dgamma_t0 = self.velocities

        # Householder decomposition in Euclidean case, updates `orthonormal_basis` in-place
        self._compute_Q(dgamma_t0, 1.)
