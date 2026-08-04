class Bivariate:
    def quanQual(dataset):
        quan = []
        qual = []
        for colum in dataset.columns:
            if dataset[colum].dtypes == "object":
                qual.append(colum)
            else:
                quan.append(colum)
        return quan, qual