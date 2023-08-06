# This file is part of sympy2c.
#
# Copyright (C) 2013-2021 ETH Zurich, Institute for Particle and Astrophysics and SIS
# ID.
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program.  If not, see <http://www.gnu.org/licenses/>.

from .utils import align


def create_interface_onary():
    return align(
        """
        |class OneAryFunction {
        |
        |    public:
        |        virtual double operator()(double) = 0;
        |        virtual double operator()(double, void *) = 0;
        |};
        """
    )


def create_curry_class(n_fixed_args):
    """creates code to implement currying of a function.  Given a
    function with n_fixed_args + 1 double arguments, the first
    n_fixed_args are frozen, such that the resulting object behaves like
    a function with one input argument of type double"""

    class_name = "Curry_{}".format(n_fixed_args)

    function_args_decl = ", ".join("double" for i in range(n_fixed_args + 1))

    default_args_decl = "\n    ".join(
        "double _v{i};".format(i=i) for i in range(n_fixed_args)
    )

    cons_args_decl = ", ".join(
        [
            "double (*f)({function_args_decl})".format(
                function_args_decl=function_args_decl
            )
        ]
        + ["double v{i}".format(i=i) for i in range(n_fixed_args)]
    )

    attributes_init = ", ".join(
        ["_f(f)"] + ["_v{i}(v{i})".format(i=i) for i in range(n_fixed_args)]
    )

    fixed_args = ", ".join(["_v{i}".format(i=i) for i in range(n_fixed_args)] + ["x"])

    code = align(
        """
        |class {class_name}: public OneAryFunction {{
        |
        |      double (*_f)({function_args_decl});
        |      {default_args_decl}
        |
        |      public:
        |           {class_name}({cons_args_decl}): {attributes_init} {{}};
        |
        |      double operator()(double x) {{
        |           return _f({fixed_args});
        |      }}
        |
        |      // for use as a gsl_function:
        |      double operator()(double x, void *) {{
        |           return _f({fixed_args});
        |      }}
        |}};"""
    ).format(
        class_name=class_name,
        function_args_decl=function_args_decl,
        default_args_decl=default_args_decl,
        cons_args_decl=cons_args_decl,
        attributes_init=attributes_init,
        fixed_args=fixed_args,
    )

    return class_name, code


if __name__ == "__main__":

    print("#include <cstdio>")
    base_class_name, base_class_decl, class_name, class_decl = create_curry_class(
        ["x", "y", "z"], ["x", "z"]
    )
    print(base_class_decl)
    print(class_decl)
    print(
        r"""

    double add3(double x, double y, double z) { return x + y + z; };

    double integrate(Function1Ary *f) {
        double sum = 0.5 * (*f)(0) + 0.5 * (*f)(1);
        double h = 0.1;
        for (int i=1; i<10; i++)
            sum += (*f)(i * h);
        return(h * sum);
    }

    int main()
    {
        Curry_3_0_2 f(add3, 1, 3);
        std::printf("should be 4: %lf\n", f(0));
        std::printf("should be 5: %lf\n", f(1));
        std::printf("should be 4.5: %lf\n", integrate(&f));

    }
    """
    )
