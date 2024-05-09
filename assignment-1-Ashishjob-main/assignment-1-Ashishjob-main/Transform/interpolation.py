class interpolation:

    def linear_interpolation(self, p1, p2, i1, i2, x):
        """Computes the linear interpolation value at some iD location x between two 1D points (Pt1 and Pt2).
        
        There are no arguments defined in the function definition on purpose. It is left upto the student to define any requierd arguments.
        Please change the signature of the function and add the arguments based on your implementation.
        
        The function ideally takes two 1D points Pt1 and Pt2, and their intensitites I(Pt1), I(Pt2).
        return the interpolated intensity value (I(x)) at location x """

        # Write your code for linear interpolation here

        I = (i1 * ((p2 - x) / (p2 - p1))) + (i2 * ((x - p1) / (p2 - p1)))

        return I

    def bilinear_interpolation(self, p1, p2, p3, p4, i1, i2, i3, i4, x):
        """Computes the bilinear interpolation value at some 2D location x between four 2D points (Pt1, Pt2, Pt3, and Pt4).
        
        There are no arguments defined in the function definition on purpose. It is left upto the student to define any requierd arguments.
        Please change the signature of the function and add the arguments based on your implementation.
        
        The function ideally takes four 2D points Pt1, Pt2, Pt3, and Pt4, and their intensitites I(Pt1), I(Pt2), I(Pt3), and I(Pt4).
        return the interpolated intensity value (I(x)) at location x """

        # Write your code for bilinear interpolation here
        # Recall that bilinear interpolation performs linear interpolation three times
        # Please reuse or call linear interpolation method three times by passing the appropriate parameters to compute this task

        tr = self.linear_interpolation(p1[1], p2[1], i1, i2, x[1])
        br = self.linear_interpolation(p3[1], p4[1], i3, i4, x[1])

        tp = [p1[0], x[1]]
        bp = [p3[0], x[1]]

        I = self.linear_interpolation(tp[0], bp[0], tr, br, x[0])

        return I
