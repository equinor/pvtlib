# Ultrasonic Meter Wet Gas Over-Reading Correction (Van Putten)

An ultrasonic meter in wet gas reads too high, because the liquid occupies part of
the pipe cross section. This example demonstrates the Van Putten over-reading
correction, which converts the indicated gas volume flow into the actual gas
volume flow.

The notebook plots the over-reading surface, then corrects a single case using
both critical gas Froude number variants: from the water-liquid ratio,
Equation (27), and from the gas Ohnesorge number, Equations (25)-(26).

All input values in the notebook are illustrative.

**Required packages**: pvtlib, numpy, pandas, matplotlib

**Format**: Jupyter Notebook

## Reference

van Putten et al., *Ultrasonic Meters in Wet Gas Application*, North Sea Flow
Measurement Workshop, 2015.
[Paper](https://nfogm.no/wp-content/uploads/2019/02/2015-02-Ultrasonic-Meters-in-Wet-Gas-Application-van-Putten-DNV-GL.pdf)

The implemented model is the simplified one, Equations (29)-(30). The full
physical model, Equation (28), is not implemented.

`within_JIP_envelope` only confirms that the gas volume fraction,
Lockhart-Martinelli parameter, density ratio and gas Froude number are inside the
ranges reported from the JIP tests. Meter type, pipe size, installation and fluids
still require engineering assessment.
