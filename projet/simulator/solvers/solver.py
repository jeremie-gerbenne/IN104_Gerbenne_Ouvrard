from ..physics.engine import *

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
        """Compute the solution of the system at t
            The input `t` given to this method should be increasing
            throughout the execution of the program.
            Return the new state at time t."""


        raise NotImplementedError


class DummySolver(ISolver):
    def integrate(self, t):
        """Compute the solution of the system at t
            The input `t` given to this method should be increasing
            throughout the execution of the program.
            Return the new state at time t."""

        t_cur=self.t0
        y=self.y0
        max_s_s =self.max_step_size
        dt = (t-t_cur)/(int((t-t_cur)/max_s_s)+1)

        while t_cur < t:
            y = y + dt * self.f(t_cur, y)
            t_cur += dt

        self.t0 = t
        self.y0 = y
        return y
        raise NotImplementedError

    pass

class LessDummySolver(ISolver):
    def integrate(self, t):
        """" Compute the solution of the system at t
            The input `t` given to this method should be increasing
            throughout the execution of the program.
            Return the new state at time t."""



        t_cur = self.t0
        y = self.y0
        n = int((y.dim)/4)
        max_s_s =self.max_step_size
        dt = (t-t_cur)/(int((t-t_cur)/max_s_s)+1)
        while t_cur < t:

            yder = self.f(t_cur,y)

            ynew = Vector(4*n)
            for i in range(n):
                ynew[2*i]=y[2*i]+dt*y[2*i+2*n]+0.5*(dt**2)*yder[2*i+2*n]
                ynew[2*i+1]=y[2*i+1]+dt*y[2*i+1+2*n] +0.5*(dt**2)*yder[2*i+1+2*n]
                ynew[2*n+2*i]=y[2*n+2*i]
                ynew[2*n+2*i+1]=y[2*n+2*i+1]

            yder2 = self.f(t_cur,ynew)

            for i in range(n):
                ynew[2*n+2*i]=y[2*n+2*i]+0.5*dt*(yder[2*i+2*n]+yder2[2*i+2*n])
                ynew[2*n+2*i+1]=y[2*n+2*i+1]+0.5*dt*(yder[2*i+2*n+1]+yder2[2*i+2*n+1])
            t_cur += dt
        self.t0 = t
        self.y0 = ynew
        return ynew
        raise NotImplementedError
    pass

