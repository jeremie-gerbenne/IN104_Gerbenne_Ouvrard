class SolverError(Exception):
    pass


class ISolver:

    # NOTE: our systems do not depend on time,
    # so the input t0 will never be used by the
    # the derivatives function f
    # However, removing it will not simplify
    # our functions so we might as well keep it
    # and build a more general library that
    # we will be able to reuse some day

    def __init__(self, f, t0, y0, max_step_size=0.01):
        self.f = f
        self.t0 = t0
        self.y0 = y0
        self.max_step_size = max_step_size

    def integrate(self, t):
        """ Compute the solution of the system at t
            The input `t` given to this method should be increasing
            throughout the execution of the program.
            Return the new state at time t.
        """
        
        t_cur = self.t0
        y = self.y0
        while t_cur < t:
            y = y + self.max_step_size * self.f(t_cur, y)
            t_cur += self.max_step_size
        self.t0 = t
        self.y0 = y
        return y
        raise NotImplementedError


class DummySolver(ISolver):
    pass
