# coding: utf8

"""
Table definition
"""
db.define_table("cliente",
      SQLField("nombre", "string"),
      SQLField("correo", "string"),
      SQLField("password", "string"),
      format = '%(nombre)s')

"""
Table definition
"""
db.define_table("proyecto",
      SQLField("id_cliente", db.cliente),
      SQLField("razon_social", "string", notnull=False, default=None),
      SQLField("lugar", "string", notnull=False, default=None))

"""
Table definition
"""
db.define_table("tipo_mantenimiento",
      SQLField("pm", "string", length=50, notnull=False, default=None))


"""
Table definition
"""
db.define_table("quimico",
      SQLField("Fe", "double", label='Fe', length=2, notnull=False, default=None),
      SQLField("Al", "double", label='Al', length=20, notnull=False, default=None),
      SQLField("Cu", "double", label='Cu', length=20, notnull=False, default=None),
      SQLField("Cr", "double", label='Cr', length=20, notnull=False, default=None),
      SQLField("Pb", "double", label='Pb', length=20, notnull=False, default=None),
      SQLField("Sn", "double", label='Sn', length=20, notnull=False, default=None),
      SQLField("Si", "double", label='Si', length=20, notnull=False, default=None),
      SQLField("Na", "double", label='Na', length=20, notnull=False, default=None),
      SQLField("Kk", "double", label='K', length=20, notnull=False, default=None),
      SQLField("Ca", "double", label='Ca', length=20, notnull=False, default=None),
      SQLField("Mg", "double", label='Mg', length=20, notnull=False, default=None),
      SQLField("Pp", "double",  label='P', length=20, notnull=False, default=None),
      SQLField("Zn", "double", label='Zn', length=20, notnull=False, default=None))

"""
Table definition
"""
db.define_table("marca",
      SQLField("tipo", "string", notnull=False, requires=IS_IN_SET({'0': 'Aceite', '1': 'Equipo', '2': 'Componente'})), # 0 componente, 1 aceite
      SQLField("nombre", "string"),
      format = '%(nombre)s')
"""
Table definition
"""
db.define_table("modelo",
      SQLField("id_marca", db.marca),
      SQLField("tipo",requires=IS_IN_SET({'0': 'Aceite', '1': 'Equipo', '2': 'Componente'})),
      SQLField("cadena", "string"))
      


"""
Table definition
"""
db.define_table("item",
      SQLField("nombre"))


"""
Table definition
"""
db.define_table("equipo",
      SQLField("id_marca", db.marca),
      SQLField("id_proyecto", db.proyecto),
      SQLField("modelo"))

"""
Table definition
"""
db.define_table("componente",
      SQLField("id_marca", db.marca),
      SQLField("id_equipo", db.equipo),
      SQLField("id_item", db.item))


"""
Table definition
"""

db.define_table("info_equipo",
      SQLField("id_equipo"),
      SQLField("id_componente", db.componente),
      SQLField("serie_equipo", "string", length=50, notnull=False, default=None),
      SQLField("serie_componente", "string", length=50, notnull=False, default=None),
      SQLField("numero_equipo", "string", length=50, notnull=False, default=None),
      SQLField("ot_cliente", "string", length=50, notnull=False, default=None),
      SQLField("ot_lubeman", "string", length=50, notnull=False, default=None),
      SQLField("uso_equipo", "double", notnull=False, default=None),
      SQLField("unidades_uso", "string", length=10, notnull=False))



"""
Table definition
"""
db.define_table("contaminacion",
      SQLField("porc_agua", "double", notnull=False, default=None),
      SQLField("porc_dilucion", "double", notnull=False, default=None),
      SQLField("cod_iso", "string", length=50, notnull=False, default=None))

"""
Table definition
"""
db.define_table("muestra",
      SQLField("fecha_toma", "date", notnull=False, default=None),
      SQLField("fecha_recepcion", "date", notnull=False, default=None),
      SQLField("fecha_reporte", "date", notnull=False, default=None),
      SQLField("cantidad_aceite", "double", notnull=False, default=None),
      SQLField("unidades_aceite", "string", length=30, notnull=False, default=None),
      SQLField("cantidad_componente", "double", notnull=False, default=None),
      SQLField("unidades_componente", "string", length=30, notnull=False, default=None))


"""
Table definition
"""
db.define_table("viscocidad",
      SQLField("nombre", requires=IS_IN_SET({'10': '10W: 10', '30': '15W40: 30', '50': '15W40: 50', '60': '15W40: 60'})))


"""
Table definition
"""
db.define_table("aceite",
      SQLField("id_marca", db.marca),
      SQLField("viscocidad", requires=IS_IN_SET({'10': '10W: 10', '30': '15W40: 30', '50': '15W40: 50', '60': '15W40: 60'})),
      SQLField("nombre", requires=IS_IN_SET({'HD': 'HD', 'FDAO': 'FDAO'})))
#      SQLField("nombre", "string", length=50, notnull=False, default=None))

"""
Table definition
"""
db.define_table("condicion_aceite",
      SQLField("viscocidad", "double", notnull=False, default=None),
      SQLField("oxidacion", "double", notnull=False, default=None),
      SQLField("soot", "double", notnull=False, default=None),
      SQLField("sulfatacion", "double", notnull=False, default=None),
      SQLField("nitracion", "integer", notnull=False, default=None))

"""
Table definition
"""
db.define_table("mantenimiento",
      SQLField("id_tipo_mantenimiento", db.tipo_mantenimiento),
      SQLField("id_aceite", db.aceite),
      SQLField("lugar_trabajo", "string", length=50, notnull=False, default=None),
      SQLField("comentario", "text", notnull=False, default=None),
      SQLField("ruta_firma", "string", notnull=False, default=None),
      SQLField("estado", "integer", notnull=False, default=None))

"""
Table definition
"""
db.define_table("reporte",
      SQLField("id_proyecto"),
      SQLField("id_componente"),
      SQLField("id_info_equipo", db.info_equipo),
      SQLField("id_contaminacion", db.contaminacion),
      SQLField("id_muestra", db.muestra),
      SQLField("id_condicion_aceite", db.condicion_aceite),
      SQLField("id_mantenimiento", db.mantenimiento),
      SQLField("id_quimico", db.quimico),
      SQLField("fecha", "date", notnull=False, default=None))


db.define_table('infra',
    Field('name_sample'),
    Field('descri'),
    Field('summ'),
    Field('pathlength'),
    Field('water'),
    Field('sooth'),
    Field('oxi'),
    Field('nitra'),
    Field('anti'),
    Field('gas'),
    Field('dies'),
    Field('sulfa'),
    Field('ethy'))
"""
Relations between tables (remove fields you don't need from requires)
"""

db.proyecto.id_cliente.requires=IS_IN_DB(db,'cliente.id','cliente.nombre')
modelo_componente = db(db.marca.tipo==2)
db.componente.id_marca.requires=IS_IN_DB(modelo_componente, 'marca.id','marca.nombre')
db.componente.id_item.requires=IS_IN_DB(db, 'item.id','item.nombre')
db.componente.id_equipo.requires=IS_IN_DB(db, 'equipo.id','equipo.modelo')
#db.item.id_marca.requires=IS_IN_DB(db, 'modelo.id','modelo.id_marca')
modelo_equipo = db(db.marca.tipo==1)
db.equipo.id_marca.requires=IS_IN_DB(modelo_equipo, 'marca.id','marca.nombre')
db.equipo.id_proyecto.requires=IS_IN_DB(db, 'proyecto.id','proyecto.razon_social')
modelo_aceite = db(db.marca.tipo==0)
db.aceite.id_marca.requires=IS_IN_DB(modelo_aceite, 'marca.id','marca.nombre')
#db.aceite.id_viscocidad.requires=IS_IN_DB(db, 'viscocidad.id','viscocidad.cantidad')
db.modelo.id_marca.requires=IS_IN_DB(db, 'marca.id','marca.nombre')
#db.info_equipo.id_equipo.requires=IS_IN_DB(db, 'equipo.id')
#record = db(db.item).select(join=db.componente.on(db.componente.id_item==db.item.id))
db.info_equipo.id_componente.requires=IS_IN_DB(db,'componente.id')
#db.reporte.id_proyecto.requires=IS_IN_DB(db, 'proyecto.id','proyecto.razon_social','proyecto.lugar')
#db.reporte.id_info_equipo.requires=IS_IN_DB(db, 'info_equipo.id','info_equipo.id_equipo','info_equipo.id_item','info_equipo.serie_equipo','info_equipo.serie_componente','info_equipo.numero_equipo','info_equipo.ot_cliente','info_equipo.ot_lubeman','info_equipo.uso_equipo','info_equipo.unidades_uso')
#db.reporte.id_contaminacion.requires=IS_IN_DB(db, 'contaminacion.id','contaminacion.porc_agua','contaminacion.porc_dilucion','contaminacion.cod_iso')
#db.reporte.id_muestra.requires=IS_IN_DB(db, 'muestra.id','muestra.fecha_toma','muestra.fecha_recepcion','muestra.fecha_reporte','muestra.cantidad_aceite','muestra.unidades_aceite','muestra.cantidad_componente','muestra.unidades_componente')
#db.reporte.id_condicion_aceite.requires=IS_IN_DB(db, 'condicion_aceite.id','condicion_aceite.viscocidad','condicion_aceite.oxidacion','condicion_aceite.soot','condicion_aceite.sulfatacion','condicion_aceite.nitracion')
#db.reporte.id_mantenimiento.requires=IS_IN_DB(db, 'mantenimiento.id','mantenimiento.id_tipo_mantenimiento','mantenimiento.id_aceite','mantenimiento.lugar_trabajo','mantenimiento.comentario','mantenimiento.ruta_firma','mantenimiento.estado')
#db.reporte.id_elemento.requires=IS_IN_DB(db,'elemento.id')
db.mantenimiento.id_tipo_mantenimiento.requires=IS_IN_DB(db, 'tipo_mantenimiento.id')
db.mantenimiento.id_aceite.requires=IS_IN_DB(db, 'aceite.id')
