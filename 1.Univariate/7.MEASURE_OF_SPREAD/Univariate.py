import pandas as pd
import numpy as np

class Univariate:
    def quanQual(dataset):
        quan = []
        qual = []
        for colum in dataset.columns:
            if dataset[colum].dtypes == "object":
                qual.append(colum)
            else:
                quan.append(colum)
        return quan, qual

    def descriptive(dataset, quan):
        descriptive = pd.DataFrame(index=['Mean','Median','Mode','Q1:25%','Q2:50%','Q3:75%','99%','Q4:100%',"IQR","1.5RULE",
                                  "LesserOutlier","GreaterOutlier","Min","Max","hasOutlier_Lower?", "hasOutlier_Higher?",
                                 "Skewness","Kurtosis","Var","Std_dev"], columns=quan)

        lesser_outliers = []
        greater_outliers = []
        
        for column in quan:
            descriptive[column]['Mean'] = dataset[column].mean()
            descriptive[column]['Median'] = dataset[column].median()
            descriptive[column]['Mode'] = dataset[column].mode()[0]
            descriptive[column]['Q1:25%'] = dataset.describe()[column]['25%']
            descriptive[column]['Q2:50%'] = dataset.describe()[column]['50%']
            descriptive[column]['Q3:75%'] = dataset.describe()[column]['75%']
            descriptive[column]['99%'] = np.percentile(dataset[column],99)
            descriptive[column]['Q4:100%'] = dataset.describe()[column]['max']
            descriptive[column]['IQR'] = descriptive[column]['Q3:75%'] - descriptive[column]['Q1:25%']
            descriptive[column]['1.5RULE'] = 1.5*descriptive[column]['IQR']
            descriptive[column]['LesserOutlier'] = descriptive[column]['Q1:25%'] - descriptive[column]['1.5RULE']
            descriptive[column]['GreaterOutlier'] = descriptive[column]['Q3:75%'] + descriptive[column]['1.5RULE']
            descriptive[column]['Min'] = dataset[column].min()
            descriptive[column]['Max'] = dataset[column].max()
            if descriptive[column]['Min'] < descriptive[column]['LesserOutlier']:
                descriptive[column]['hasOutlier_Lower?'] = "YES"
                lesser_outliers.append(column)
            else:
                descriptive[column]['hasOutlier_Lower?'] = "NO"
                
            if descriptive[column]['Max'] > descriptive[column]['GreaterOutlier']:
                descriptive[column]['hasOutlier_Higher?'] = "YES"
                greater_outliers.append(column)
            else:
                descriptive[column]['hasOutlier_Higher?'] = "NO"
        
            descriptive[column]['Skewness'] = dataset[column].skew()
            descriptive[column]['Kurtosis'] = dataset[column].kurtosis()
            descriptive[column]['Var'] = dataset[column].var()
            descriptive[column]['Std_dev'] = dataset[column].std()
        
        return descriptive, lesser_outliers, greater_outliers

    def get_distribution_plot(dataset, column):
        from matplotlib import pyplot
        from scipy.stats import norm
        import seaborn as sns

        ax = sns.distplot(dataset, kde=True, kde_kws={'color':'blue'}, color='Green')

        mean_val = dataset.mean()
        std_dev = dataset.std()
        
        pyplot.axvline(dataset.mean(), color='red', linestyle='-', linewidth=2, label=f'Mean: {mean_val:.2f}')
        pyplot.legend()
        
        print('Mean=%.3f, Standard deviation=%.3f'%(dataset.mean(), dataset.std()))
        pyplot.title(f'Distribution of {column}\nMean={mean_val:.2f}\nStd Devd={std_dev:.2f}')

        # #define distribution
        # dist = norm(dataset.mean(), dataset.std())

        # #probabilities for a range of outcomes
        # values = [value for value in range(startrange, endrange)]
        # probabilities = [dist.pdf(value) for value in values]

        # print("The area between range ({},{}):{}".format(startrange, endrange, sum(probabilities)))

        # return sum(probabilities)