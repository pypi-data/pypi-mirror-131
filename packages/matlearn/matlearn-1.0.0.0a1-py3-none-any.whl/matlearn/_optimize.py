import numpy as np
from matlearn.evaluation import *
from matlearn.preprocessing import split_train_test
from matlearn.models import LinearRegressor, LogisticRegressor


class Optimization:

    cost_hist = list()

    def __init__(self):
        pass

    def _check_params(self):

        if self.lr < .0000000001:
            raise ValueError(f'Learning rate must be greater than {self.lr}')
        if self.n_iter_per_epoch < 1:
            raise ValueError(
                'n_iter_per_epoch must be equal or greater than 1.')

    def _set_target(self, y):
        size = np.unique(y).size
        if isinstance(self, LinearRegressor):
            self._app_loss = 'mse'
            self._target_type = 'continuous'
            self._multiclass = False
        elif isinstance(self, LogisticRegressor):
            self._target_type = 'discrete'
            if size == 2:
                self._app_loss = 'binary_cross_entropy'
                self._multiclass = False
            elif size > 2:
                self._app_loss = 'cross_entropy'
                self._multiclass = True

    @staticmethod
    def _weight_grad(x, y, p): return 1/len(x) * np.dot(x.T, (p-y))

    @staticmethod
    def _bias_grad(y, p): return np.average(p - y)

    def GD(self, x, y):
        '''Gradient descent algorithm.
        '''
        self._check_params()
        self._set_target(y)
        if self._target_type == 'discrete':
            self._target_unique_values = np.unique(y)
        self._trained = True
        epoch = 1
        counter = 0
        if y.ndim == 1:
            y = y.reshape(-1,1)

        self.weight = np.random.randn(x.shape[1], 1)
        if self._multiclass:
            self.weight = np.random.randn(x.shape[1], y.shape[1])

        if self.train_bias:
            self.bias = np.ones((self.weight.shape[1],))

        # starting the algorithm
        while epoch != self.maxEpoch+1:

            if self.n_reports > 0:
                print(f'''\n\n **** EPOCH {epoch} ****\n''')

            iterNum = 1
            list_idx = np.array_split(
                np.random.permutation(len(x)), self.n_iter_per_epoch)

            for idx in list_idx:

                xit_train, yit_train = x[idx], y[idx]

                if self.use_validation:
                    xit_train, xit_val, yit_train, yit_val = split_train_test(
                        x[idx], y[idx], shuffle=False, train_ratio=1 - (self.val_ratio))
                    if self._target_type == 'discrete':
                        p_val = self.predict_proba(xit_val)
                    else:
                        p_val = self.predict(xit_val)

                if self._target_type == 'discrete':
                    p_train = self.predict_proba(xit_train)
                else:
                    p_train = self.predict(xit_train)

                if self.train_bias:
                    self.bias = (self.bias) - (self.lr *
                                               Optimization._bias_grad(yit_train, p_train))
                self.weight = self.weight - \
                    (self.lr * Optimization._weight_grad(xit_train, yit_train, p_train))

                dl_train, rl_train = Loss._use_app_loss(self._app_loss)(
                    p_train, yit_train), regularization(self.weight, type=self.regulariz_type, alpha=self.alpha)

                if self.use_validation:
                    dl_val, rl_val = Loss._use_app_loss(self._app_loss)(
                        p_val, yit_val), regularization(self.weight, type=self.regulariz_type, alpha=self.alpha)
                Optimization.cost_hist.append(dl_train + rl_train)

                if self.n_reports > 0:
                    if self.use_validation:
                        print('iteration {:3d}: training loss = {:.2f}  |   validation loss = {:.2f}'.format(
                            iterNum, Optimization.cost_hist[-1], dl_val + rl_val ))
                    else:
                        print('iter {:3d}: training loss = {:.2f}'.format(
                            iterNum, Optimization.cost_hist[-1]))
                iterNum += 1

                try:
                    if abs(Optimization.cost_hist[-1] - Optimization.cost_hist[-2]) < self.converLim:
                        counter += 1
                    if counter == self.n_converLim:
                        print('End of the algorithm at iteration number {}.\nThe differences in costs is less than {}'.format(
                            epoch, self.converLim))
                        return
                except IndexError:
                    pass
            self.n_reports -= 1
            epoch += 1
        ##########################################################