from ..utils.vector import Vector, Vector2
from .constants import G


def gravitational_force(pos1, mass1, pos2, mass2):
    """ Return the force applied to a body in pos1 with mass1
        by a body in pos2 with mass2
    """
    u_12 = pos2-pos1
    r = Vector.norm(u_12)
    return u_12*G*mass1*mass2/r**3
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

    def derivatives(self, t0, y0):
        n = len(y0)/4
        n = int(n)
        y = Vector(4*n)
        for i in range(n):
            y[2*i]=y0[2*i+2*n]
            y[2*i+1]=y0[2*i+1+2*n]
            force = Vector2(0,0)
            corps_i = self.world.get(i)
            pos_i = Vector2(y0[2*i],y0[2*i+1])
            mass_i = corps_i.mass
            for j in range(n):
                if i!=j:
                    corps_j = self.world.get(j)
                    pos_j = Vector2(y0[2*j],y0[2*j+1])
                    mass_j = corps_j.mass
                    Fij = gravitational_force(pos_i,mass_i,pos_j,mass_j)
                    force = force + Fij
            y[2*i+2*n] = Vector2.get_x(force)/mass_i
            y[2*i+1+2*n] = Vector2.get_y(force)/mass_i
        return y

    def make_solver_state(self):
        n = len(self.world)
        y = Vector(4*n)
        for i in range(n) :
            corps_i = self.world.get(i)
            pos_i = corps_i.position
            y[2*i] = Vector2.get_x(pos_i)
            y[2*i+1] = Vector2.get_y(pos_i)

        for i in range(n) :
            corps_i = self.world.get(i)
            vel_i = corps_i.velocity
            y[2*n+2*i] = Vector2.get_x(vel_i)
            y[2*n+2*i+1] = Vector2.get_y(vel_i)
        return y

class LessDummyEngine(IEngine):
    def derivatives(self, t0, y0):
        n = len(y0)/4
        n = int(n)
        y = Vector(4*n)
        for i in range(n):
            y[2*i]=y0[2*i+2*n]
            y[2*i+1]=y0[2*i+1+2*n]
            force = Vector2(0,0)
            corps_i = self.world.get(i)
            pos_i = corps_i.position
            mass_i = corps_i.mass
            for j in range(i+1,n):
                corps_j = self.world.get(j)
                pos_j = corps_j.position
                mass_j = corps_j.mass
                Fij = gravitational_force(pos_i,mass_i,pos_j,mass_j)
                y[2*n+2*i] = Vector2.get_x(Fij)/mass_i
                y[2*i+1+2*n] = Vector2.get_y(Fij)/mass_i
                y[2*n+2*j] = Vector2.get_x(-1*Fij)/mass_j
                y[2*j+1+2*n] = Vector2.get_y(-1*Fij)/mass_j
        return y

    def make_solver_state(self):
        n = len(self.world)
        y = Vector(4*n)
        for i in range(n) :
            corps_i = self.world.get(i)
            pos_i = corps_i.position
            y[2*i] = Vector2.get_x(pos_i)
            y[2*i+1] = Vector2.get_y(pos_i)

        for i in range(n) :
            corps_i = self.world.get(i)
            vel_i = corps_i.velocity
            y[2*n+2*i] = Vector2.get_x(vel_i)
            y[2*n+2*i+1] = Vector2.get_y(vel_i)
        return y
