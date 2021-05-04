from ..utils.vector import Vector, Vector2
from .constants import G


def gravitational_force(pos1, mass1, pos2, mass2):
    """ Return the force applied to a body in pos1 with mass1
        by a body in pos2 with mass2
    """
    raise NotImplementedError


class IEngine:
    def __init__(self, world):
        self.world = world

    def derivatives(self, t0, y0):
        """ This is the method that will be fed to the solver
            it does not use it's first argument t0,
            its second argument y0 is a vector containing the positions 
            and velocities of the bodies, it is laid out as follow
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.

            Return the derivative of the state, it is laid out as follow
                [vx1, vy1, vx2, vy2, ..., vxn, vyn, ax1, ay1, ax2, ay2, ..., axn, ayn]
            where vxi, vyi are the velocities and axi, ayi are the accelerations.
        """
        n = len(y0)/4
        for i in range(n):
            y0[2*i]=y0[2*i+2*n]
            y0[2*i+1]=y0[2*i+1+2*n]
            force = Vector2(0,0)
            corps_i = self.world[i]
            pos_i = corps_i.pos
            mass_i = corps_i.mass
            for j in range(n):
                if i!=j:
                    corps_j = self.world[j]
                    pos_j = corps_j.pos
                    mass_j = corps_j.mass
                    Fij = gravitational_force(pos_i,mass_i,pos_j,mass_j)
                    force = force + Fij
            y0[2*i+2*n] = Vector2.get_x(force)
            y0[2*i+1+2*n] = Vector2.get_y(force)
        return y0
        
        raise NotImplementedError

    def make_solver_state(self):
        """ Returns the state given to the solver, it is the vector y in
                y' = f(t, y)
            In our case, it is the vector containing the 
            positions and speeds of all our bodies:
                [x1, y1, x2, y2, ..., xn, yn, vx1, vy1, vx2, vy2, ..., vxn, vyn]
            where xi, yi are the positions and vxi, vyi are the velocities.
        """
        raise NotImplementedError


class DummyEngine(IEngine):
    pass
