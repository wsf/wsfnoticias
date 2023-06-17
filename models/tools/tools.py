def aplica_regla(titulo, cuerpo, copete, reglas):
    regla_nombre = ""

    for r in reglas:
        terminos = r.terminos_or

        for t in terminos:

            condi_titulo = t in titulo
            condi_cuerpo = t in cuerpo
            condi_copete = t in copete

            condi = condi_copete or condi_titulo or condi_cuerpo

            if condi:
                regla_nombre += r.nombre_regla

    return regla_nombre