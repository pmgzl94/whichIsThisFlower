import numpy

class AdamConv():
    def __init__(self, alpha=0.001, b1=0.9, b2=0.999, epsilon=1e-08):
        self.t = 1

        self.b1 = b1
        self.b2 = b2
        self.alpha = alpha
        self.eps = epsilon

    def setMomentumVars(self, ws, bs):
        self.mw = numpy.zeros(ws.shape)
        self.vw = numpy.zeros(ws.shape)
        self.mb = numpy.zeros(bs.shape)
        self.vb = numpy.zeros(bs.shape)

    def generic_update(self, m, v, g, curr_val):
        new_m = self.b1 * m + (1 - self.b1) * g
        new_v = self.b2 * v + (1 - self.b2) * g**2
        
        b1t = self.b1**self.t
        b2t = self.b2**self.t

        mhat = new_m / (1 - b1t)
        vhat = new_v / (1 - b2t)

        updated_val = curr_val - self.alpha * mhat / (numpy.sqrt(vhat) + self.eps)

        return updated_val, new_m, new_v

    def update(self, ws, bs, g_ws, g_bs):
        self.t = self.t + 1

        new_ws, self.mw, self.vw = self.generic_update(self.mw, self.vw, g_ws, ws)
        
        new_bs, self.mb, self.vb = self.generic_update(self.mb, self.vb, g_bs, bs)

        return new_ws, new_bs

class AdamFC():
    def __init__(self, alpha=0.001, b1=0.9, b2=0.999, epsilon=1e-08):
        self.t = 1

        self.b1 = b1
        self.b2 = b2
        self.alpha = alpha
        self.eps = epsilon

    def setMomentumVars(self, ws, bs):
        
        self.mw = []
        self.vw = []
        
        self.mb = []
        self.vb = []
        
        ## init momentums (moving average and squarred grad)
        for i in range(len(ws)):
            n_mw = numpy.zeros(ws[i].shape)
            self.mw.append(n_mw)

            n_vw = numpy.zeros(ws[i].shape)
            self.vw.append(n_vw)

            n_mb = numpy.zeros(bs[i].shape)
            self.mb.append(n_mb)

            n_vb = numpy.zeros(bs[i].shape)
            self.vb.append(n_vb)

    def generic_update(self, m, v, g, curr_val):
        
        nb_layer = len(m)
        new_m = []
        new_v = []

        for i in range(nb_layer):
            mt = self.b1 * m[i] + (1 - self.b1) * g[i]
            vt = self.b2 * v[i] + (1 - self.b2) * g[i]**2
            new_m.append(mt)
            new_v.append(vt)

        b1t = self.b1**self.t
        b2t = self.b2**self.t

        mhat = []
        vhat = []

        for i in range(nb_layer):
            # new_m[i] = self.b1 * m[i] + (1 - self.b1) * g[i]
            # new_v[i] = self.b2 * v[i] + (1 - self.b2) * g[i]**2
            mh = new_m[i] / (1 - b1t)
            vh = new_v[i] / (1 - b2t)
            mhat.append(mh)
            vhat.append(vh)

        updated_params = []

        for i in range(nb_layer):
            u_val = curr_val[i] - self.alpha * mhat[i] / (numpy.sqrt(vhat[i]) + self.eps)
            updated_params.append(u_val)

        return updated_params, new_m, new_v

    def update(self, ws, bs, nabla_w, nabla_b):
        self.t = self.t + 1

        new_ws, self.mw, self.vw = self.generic_update(self.mw, self.vw, nabla_w, ws)

        new_bs, self.mb, self.vb = self.generic_update(self.mb, self.vb, nabla_b, bs)

        return new_ws, new_bs

