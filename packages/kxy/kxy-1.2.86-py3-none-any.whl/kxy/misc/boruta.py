#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import numpy as np
import pandas as pd
from scipy.stats import binom

from tqdm import tqdm

class Boruta(object):
	def __init__(self, learner_func):
		''' '''
		self.selected_variables = []
		self.learner_func = learner_func


	def fit(self, x_df, y_df, n_evaluations=20, pval=0.95):
		''' '''
		columns = [_ for _ in x_df.columns]
		y = y_df.values

		hits = {col: 0 for col in columns}

		for _ in tqdm(range(n_evaluations)):
			# Construct shaddow features
			train_x_df = pd.DataFrame(x_df.sample(frac=1).values, \
				index=x_df.index, columns=['shaddow_%s' % col for col in columns])

			# Add to real features
			train_x_df = pd.concat([x_df, train_x_df], axis=1)
			all_columns = [_ for _ in train_x_df.columns]

			# Fit the model
			x = train_x_df[all_columns].values
			current_n_vars = len(all_columns)
			m = self.learner_func(n_vars=current_n_vars)
			m.fit(x, y)

			# Increase the hit count
			importances = [_ for _ in m.feature_importances_]
			hit_threshold = np.max([np.abs(importances[i]) \
				for i in range(current_n_vars) if all_columns[i].startswith('shaddow_')])

			for i in range(current_n_vars):
				if not all_columns[i].startswith('shaddow_') and np.abs(importances[i]) > hit_threshold:
					hits[all_columns[i]] = hits[all_columns[i]] + 1

		# Testing whether the number of hits is statistically significant to conclude the feature is important.
		# H0: We can't tell if a feature is important or not. Said differently, there is 50% chance that a feature will be a 'hit' in a round.
		# H1: A feature is important.
		# H2: A feature is unimportant.

		# Under H0, the number of hits after n_evaluations trials should be in [hm, hM] with probability pval, where hm and hM are binomial quantiles.
		# We reject H0 and accept H1 when a feature's number of hits exceeds hM.
		# We reject H0 and accept H2 when a feature's number of hits is lower than hm. 
		cdfs = binom.cdf([hits[col] for col in columns], n_evaluations, 0.5)
		selected_variables = [columns[i] for i in range(len(columns)) if cdfs[i] > pval]
		associated_hits = [hits[col] for col in selected_variables]

		self.selected_variables = [col for _,  col in sorted(zip(associated_hits, selected_variables), reverse=True)]
		self.ambiguous_variables = [columns[i] for i in range(len(columns)) if cdfs[i] <= pval and cdfs[i] >= 1.-pval]

		if self.ambiguous_variables:
			logging.warning('Features %s have not been determined important or unimportant. Consider increasing n_evaluations.' % \
				str(self.ambiguous_variables))

		if self.selected_variables == []:
			logging.warning('No variable/feature was deemed important by the model.')
			return None

		# Keep only important features and retrain the model.
		x = x_df[self.selected_variables].values
		n_vars = len(self.selected_variables)
		m = self.learner_func(n_vars=n_vars)
		m.fit(x, y)

		return m


