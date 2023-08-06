#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import numpy as np
from tqdm import tqdm

class RFE(object):
	def __init__(self, learner_func):
		''' '''
		self.selected_variables = []
		self.learner_func = learner_func


	def fit(self, x_df, y_df, n_vars):
		''' '''
		columns = [_ for _ in x_df.columns]
		y = y_df.values

		# Fit the model
		x = x_df[columns].values
		current_n_vars = len(columns)
		m = self.learner_func(n_vars=current_n_vars)
		m.fit(x, y)
		importances = [_ for _ in m.feature_importances_]

		n_rounds = max(current_n_vars-n_vars, 0)
		for _ in tqdm(range(n_rounds)):
			# Remove the least important variable
			importances = [_ for _ in m.feature_importances_]
			least_important_ix = np.argmin(np.abs(importances))
			importances.pop(least_important_ix)
			least_important_feature = columns[least_important_ix]
			logging.info('Deleting feature %s' % least_important_feature)
			columns.remove(least_important_feature)
			current_n_vars = len(columns)

			# Re-fit the model
			x = x_df[columns].values
			m = self.learner_func(n_vars=current_n_vars)
			m.fit(x, y)

		self.selected_variables = [col for _,  col in sorted(zip(importances, columns), reverse=True)]

		return m