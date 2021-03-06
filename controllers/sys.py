import datetime

@auth.requires_login()
def company():
	registros = db(db.cliente).select()
	return locals()

def project():
	registros=db(db.proyecto).select(join=db.cliente.on(db.cliente.id==db.proyecto.id_cliente),orderby=~db.proyecto.id)
	return locals()

def equipment():
	if request.args(0):
		session.proyecto=request.args(0)
		#registros=db(db.equipo.id_proyecto==session.proyecto).select(join=db.proyecto.on(db.proyecto.id==db.equipo.id_proyecto),orderby=db.equipo.id)
		rows= db((db.equipo.id_proyecto==session.proyecto)&(db.equipo.id_marca==db.marca.id)&(db.proyecto.id==db.equipo.id_proyecto)).select()
	else:
		rows= db((db.equipo.id_marca==db.marca.id)&(db.proyecto.id==db.equipo.id_proyecto)).select()
		#registros=db(db.equipo).select(join=db.proyecto.on(db.proyecto.id==db.equipo.id_proyecto),orderby=db.equipo.id)
	return locals()

def component():
	if request.args(0):
		session.equipo=request.args(0)
		#registros=db(db.componente.id_equipo==request.args(0)).select()
		rows= db((db.componente.id_equipo==session.equipo)&(db.componente.id_marca==db.marca.id)&(db.componente.id_equipo==db.equipo.id)&(db.item.id==db.componente.id_item)).select()
	else:
		#registros=db(db.componente).select()
		rows= db((db.componente.id_marca==db.marca.id)&(db.componente.id_item==db.item.id)&(db.componente.id_equipo==db.equipo.id)).select()
	return locals()

def analysis():
	session.componente=request.args(0)
	registros = db(db.reporte.id_componente==session.componente).select() 
	return locals()	

def companyCRUD():
    if len(request.args)==1:
        registro = db.cliente(request.args(0)) or redirect(URL('index'))       
    else:
        registro = None   
        #form = SQLFORM(db.pregunta, request.args[0], deletable=False, upload=URL('download'))
    form = SQLFORM(db.cliente, registro, deletable=True, showid=False, upload=URL('download'), submit_button=T("Save"))
       
    if form.process(session=None, formname='cliente').accepted:
        response.flash = 'Ok'
        redirect(URL('sys','company'))
    elif form.errors:
        response.flash = 'Error'
    return locals()	

def projectCRUD():
    if len(request.args)==1:
        registro = db.proyecto(request.args(0)) or redirect(URL('index'))       
    else:
        registro = None   
        #form = SQLFORM(db.pregunta, request.args[0], deletable=False, upload=URL('download'))
    form = SQLFORM(db.proyecto, registro, deletable=True, showid=False, upload=URL('download'), submit_button=T("Save"))
       
    if form.process(session=None, formname='proyecto').accepted:
        response.flash = 'Ok'
        redirect(URL('sys','project'))
    elif form.errors:
        response.flash = 'Error'
    return locals()

def analysisCRUD():

	if len(request.args)==1:
		record=db(db.reporte.id==request.args(0)).select().first()
		i1=record.id_mantenimiento
		i2=record.id_condicion_aceite
		i3=record.id_muestra
		i4=record.id_contaminacion
		i5=record.id_info_equipo
		i6=record.id_quimico
		session.report=request.args(0)
	else:
		redirect(URL('sys','company'))

	'''
	Formularios para agregar
	'''


	form_aceite = SQLFORM(db.aceite, None, upload=URL('download'), submit_button=T("Save"))
	if form_aceite.process(session=None, formname='aceite').accepted:
		response.flash = 'Ok'
		#Valor insertado es form_aceite.vars.id
		db(db.mantenimiento.id==i1).update(id_aceite=form_aceite.vars.id)
		redirect(URL('sys','analysisCRUD',args=[session.report]))
	elif form_aceite.errors:
		response.flash = 'Error'

	form_tipo_mantenimiento = SQLFORM(db.tipo_mantenimiento, None, upload=URL('download'), submit_button=T("Save"))
	if form_tipo_mantenimiento.process(session=None, formname='tipo_mantenimiento').accepted:
		response.flash = 'Ok'
		#Valor insertado es form_tipo_mantenimiento.vars.id
		db(db.mantenimiento.id==i1).update(id_tipo_mantenimiento=form_tipo_mantenimiento.vars.id)
		redirect(URL('sys','analysisCRUD',args=[session.report]))
	elif form_tipo_mantenimiento.errors:
		response.flash = 'Error'

	'''
	form_equipo = SQLFORM(db.equipo, None, upload=URL('download'))
	if form_equipo.process(session=None, formname='equipo').accepted:
		response.flash = 'Ok'
		#Valor insertado es form_equipo.vars.id
		db(db.info_equipo.id==i5).update(id_equipo=form_equipo.vars.id)
		redirect(URL('sys','analysisCRUD',args=[session.report]))
	elif form_equipo.errors:
		response.flash = 'Error'

	form_componente = SQLFORM(db.componente, None, upload=URL('download'))
	if form_componente.process(session=None, formname='componente').accepted:
		response.flash = 'Ok'
		#Valor insertado es form_componente.vars.id
		db(db.info_equipo.id==i5).update(id_componente=form_componente.vars.id)
		redirect(URL('sys','analysisCRUD',args=[session.report]))
	elif form_componente.errors:
		response.flash = 'Error'

	'''

	'''
	Formularios para editar
	'''
	registro = db.mantenimiento(i1) or redirect(URL('index'))
	form1 = SQLFORM(db.mantenimiento, registro, showid=False, upload=URL('download'), submit_button=T("Save"))       
	if form1.process(session=None, formname='mantenimiento').accepted:
		response.flash = 'Ok'
		redirect(URL('sys','analysisCRUD',args=[session.report]))
	elif form1.errors:
		response.flash = 'Error'

	registro = db.condicion_aceite(i2) or redirect(URL('index'))
	form2 = SQLFORM(db.condicion_aceite, registro, showid=True, upload=URL('download'), submit_button=T("Save"))       
	if form2.process(session=None, formname='condicion_aceite').accepted:
		response.flash = 'Ok'
		redirect(URL('sys','analysisCRUD',args=[session.report]))
	elif form2.errors:
		response.flash = 'Error'

	registro = db.muestra(i3) or redirect(URL('index'))
	form3 = SQLFORM(db.muestra, registro, showid=False, upload=URL('download'), submit_button=T("Save"))       
	if form3.process(session=None, formname='muestra').accepted:
		response.flash = 'Ok'
		redirect(URL('sys','analysisCRUD',args=[session.report]))
	elif form3.errors:
		response.flash = 'Error'

	registro = db.contaminacion(i4) or redirect(URL('index'))
	form4 = SQLFORM(db.contaminacion, registro, showid=True, upload=URL('download'), submit_button=T("Save"))       
	if form4.process(session=None, formname='contaminacion').accepted:
		response.flash = 'Ok'
		redirect(URL('sys','analysisCRUD',args=[session.report]))
	elif form4.errors:
		response.flash = 'Error'

	registro = db.info_equipo(i5) or redirect(URL('index'))
	form5 = SQLFORM(db.info_equipo, registro, showid=False, upload=URL('download'), submit_button=T("Save"))       
	if form5.process(session=None, formname='info_equipo').accepted:
		response.flash = 'Ok'
		redirect(URL('sys','analysisCRUD',args=[session.report]))
	elif form5.errors:
		response.flash = 'Error'

	registro = db.quimico(i6) or redirect(URL('index'))
	form6 = SQLFORM(db.quimico, registro, showid=True, upload=URL('download'), submit_button=T("Save"))       
	if form6.process(session=None, formname='quimico').accepted:
		response.flash = 'Ok'
		redirect(URL('sys','analysisCRUD',args=[session.report]))
	elif form6.errors:
		response.flash = 'Error'

	return locals()	

def equipmentCRUD():
	if len(request.args)==1:
		registro = db.equipo(request.args(0)) or redirect(URL('index'))       
	else:
		registro = None   
        #form = SQLFORM(db.pregunta, request.args[0], deletable=False, upload=URL('download'))
	form = SQLFORM(db.equipo, registro, deletable=True, showid=False, upload=URL('download'), submit_button=T("Save"))
       
	if form.process(session=None, formname='equipo').accepted:
		response.flash = 'Ok'
		redirect(URL('sys','equipment',args=[session.proyecto]))
	elif form.errors:
		response.flash = 'Error'
	return locals()

def componentCRUD():
	if len(request.args)==1:
		registro = db.componente(request.args(0)) or redirect(URL('index'))       
	else:
		registro = None   
        #form = SQLFORM(db.pregunta, request.args[0], deletable=False, upload=URL('download'))
	form = SQLFORM(db.componente, registro, deletable=True, showid=False, upload=URL('download'), submit_button=T("Save"))
       
	if form.process(session=None, formname='componente').accepted:
		response.flash = 'Ok'
		redirect(URL('sys','component',args=[session.equipo]))
	elif form.errors:
		response.flash = 'Error'
	return locals()

def insertReport():
	i1=db.mantenimiento.insert(id_tipo_mantenimiento=1, id_aceite=1, lugar_trabajo='', comentario='', ruta_firma='', estado=0)
	i2=db.condicion_aceite.insert(viscocidad=0, oxidacion=0, soot=0, sulfatacion=0, nitracion=0)
	i3=db.muestra.insert(fecha_toma=datetime.datetime.today(), fecha_recepcion=datetime.datetime.today(), fecha_reporte=datetime.datetime.today(), cantidad_aceite=0, unidades_aceite='', cantidad_componente=0, unidades_componente='')
	i4=db.contaminacion.insert(porc_agua=0, porc_dilucion=0, cod_iso='')
	i5=db.info_equipo.insert(id_equipo=session.equipo, id_componente=session.componente, serie_equipo='', serie_componente='', numero_equipo='', ot_cliente='', ot_lubeman='', uso_equipo=0, unidades_uso='')
	i6=db.quimico.insert(Fe=0,Al=0,Cu=0,Cr=0,Pb=0,Sn=0,Si=0,Na=0,Kk=0,Ca=0,Mg=0,Pp=0,Zn=0)

	session.reporte=db.reporte.insert(id_proyecto=session.proyecto, id_componente=session.componente, id_info_equipo=i5, id_contaminacion=i4, id_muestra=i3, id_condicion_aceite=i2, id_mantenimiento=i1, id_quimico=i6, fecha=datetime.datetime.today())
	return True

def newAnalysis():
	#insertar valores por defecto, luego se editan.
	insertReport()
	redirect(URL('sys','analysisCRUD',args=[session.reporte]))

def newBulkAnalysis():
	var_idequipo=request.args(0)
	var_proyecto=request.args(1)
	try:
		records=db(db.componente.id_equipo==var_idequipo).select()
		for record in records:
			session.equipo=var_idequipo
			session.proyecto=var_proyecto
			session.componente=record.id
			insertReport()
		redirect(URL('sys','equipment',args=[session.proyecto]))		
	except Exception, e:
		redirect(URL('sys','equipment',args=[session.proyecto]))

def data():
	if request.args(0)==None:	
		pass
	elif request.args(0)=='form1':
		registro = db.quimico(request.args(1)) or redirect(URL('data'))
		form = SQLFORM(db.quimico, registro, showid=True, upload=URL('download'), submit_button=T("Save"))       
		if form.process(session=None, formname='quimico').accepted:
			response.flash = 'Ok'
			redirect(URL('sys','data'))
		elif form.errors:
			response.flash = 'Error'	
	elif request.args(0)=='form2':
		registro = db.contaminacion(request.args(1)) or redirect(URL('data'))
		form = SQLFORM(db.contaminacion, registro, showid=True, fields=['porc_agua','porc_dilucion'], upload=URL('download'), submit_button=T("Save"))       
		if form.process(session=None, formname='contaminacion').accepted:
			response.flash = 'Ok'
			redirect(URL('sys','data'))
		elif form.errors:
			response.flash = 'Error'
	elif request.args(0)=='form3':
		registro = db.condicion_aceite(request.args(1)) or redirect(URL('data'))
		form = SQLFORM(db.condicion_aceite, registro, showid=True, fields=['oxidacion','soot','sulfatacion','nitracion'], upload=URL('download'), submit_button=T("Save"))       
		if form.process(session=None, formname='condicion_aceite').accepted:
			response.flash = 'Ok'
			redirect(URL('sys','data'))
		elif form.errors:
			response.flash = 'Error'
	elif request.args(0)=='form4':
		registro = db.contaminacion(request.args(1)) or redirect(URL('data'))
		form = SQLFORM(db.contaminacion, registro, showid=True, fields=['cod_iso'], upload=URL('download'), submit_button=T("Save"))       
		if form.process(session=None, formname='contaminacion').accepted:
			response.flash = 'Ok'
			redirect(URL('sys','data'))
		elif form.errors:
			response.flash = 'Error'
	elif request.args(0)=='form5':
		registro = db.condicion_aceite(request.args(1)) or redirect(URL('data'))
		form = SQLFORM(db.condicion_aceite, registro, showid=True, fields=['viscocidad'], upload=URL('download'), submit_button=T("Save"))       
		if form.process(session=None, formname='condicion_aceite').accepted:
			response.flash = 'Ok'
			redirect(URL('sys','data'))
		elif form.errors:
			response.flash = 'Error'
	return locals()

def confirmation_pdf():

    # Let's import the wrapper
    import pdf
    from pdf.theme import colors, DefaultTheme
    from reportlab.lib.styles import ParagraphStyle, PropertySet
    from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER, TA_JUSTIFY
    from reportlab.platypus import Paragraph
    # and define a constant
    TABLE_WIDTH = 250 # this you cannot do in rLab which is why I wrote the helper initially

    # then let's extend the Default theme. I need more space so I redefine the margins
    # also I don't want tables, etc to break across pages (allowSplitting = False)
    # see http://www.reportlab.com/docs/reportlab-userguide.pdf
    class MyTheme(DefaultTheme):
        from reportlab.lib.units import inch
        doc = {
            #'pagesize': (11.69*inch,8.26*inch),
            'pagesize': (8*inch,8.26*inch),
            'leftMargin': 25,
            'rightMargin': 25,
            'topMargin': 10,
            'bottomMargin': 25,
            'allowSplitting': False,
            }
    class ParagraphStyle(PropertySet):
        defaults = {
        'fontName':'Helvetica',
        'fontSize':10,
        'leading':6,
        'leftIndent':0,
        'rightIndent':0,
        'firstLineIndent':0,
        'alignment':TA_LEFT,
        'spaceBefore':0,
        'spaceAfter':0,
        'bulletFontName':'Helvetica',
        'bulletFontSize':10,
        'bulletIndent':0,
        'textColor': 'black',
        'backColor':None,
        'wordWrap':None,
        'borderWidth': 0,
        'borderPadding': 0,
        'borderColor': None,
        'borderRadius': None,
        'allowWidows': 1,
        'allowOrphans': 0,
        'textTransform': None,
        'endDots': None
        }

    p = ParagraphStyle('test')
    p.leading = 7
    p.fontSize = 6
    # let's create the doc and specify title and author
    doc = pdf.Pdf('Reporte de Fluidos', 'Lubeman')

    # now we apply our theme
    doc.set_theme(MyTheme)
    # time to add the logo at the top right
    logo_path = request.folder + 'static/images/full.png'
    #doc.add_image(logo_path, 90, 100, pdf.LEFT)

    # give me some space
    #doc.add_spacer()
    
    # this header defaults to H1
    doc.add_header('Reporte de Análisis de Fluidos')

    # here's how to add a paragraph
    #doc.add_paragraph("Lubeman")
 
    #doc.add_spacer()

    # a subheader - H2
    #doc.add_header("Texto", pdf.H2)

    # as in pre-css days we wrap the address and the Google Map Image in a table
    # my wrapper module just reexposes the reportlab Paragraph and Table classes. 
    # See __init__.py in the source section below 

    # let's get the map image
    #gmap = pdf.Image("https://chart.googleapis.com/chart?chxt=x,y,r&chxr=0,0,500|1,0,200|2,1000,0&cht=lc&chd=s:cEAELFJHHHKUju9uuXUc&chco=76A4FB&chls=2.0&chs=200x125", 250,150)

    # and add both the address and the map wrapped in a table to our doc
    # UGLY inline stuff
       
    #doc.add_spacer()

    #doc.add_header('Reporte', pdf.H2)

    
   # let's move on to the divers table
   # ie_table = [['Información del Equipo','']] # this is the header row 
   # ie_table.append(['Número de Equipo', 'asd']) # these are the other rows
   # ie_table.append(['Marca de Equipo', 'asd'])
   # ie_table.append(['Modelo de Equipo', 'asd'])
   # ie_table.append(['Serie de Equipo', 'asd'])
   # ie_table.append(['Horas/Km de Equipo', 'asd'])
   # ie_table.append(['Componente', 'asd'])
   # ie_table.append(['Marca de Componente', 'asd'])
   # ie_table.append(['Modelo de Componente', 'asd'])
   # ie_table.append(['Nº serie de Componente', 'asd'])
   # ie_table.append(['O/T Cliente', 'asd'])
   # ie_table.append(['O/T Lubeman', 'asd'])
    
   # doc.add_table(ie_table, TABLE_WIDTH)
   # doc.add_spacer()
    
   # im_table = [['Información de Mantenimiento','']] # this is the header row 
   # im_table.append(['Lugar de Trabajo', 'asd']) # these are the other rows
   # im_table.append(['Marca Aceite', 'asd'])
   # im_table.append(['Nombre Aceite', 'asd'])
   # im_table.append(['Visc en Etiqueta', 'asd'])
   # im_table.append(['PM', 'asd'])
    
   # doc.add_table(im_table, TABLE_WIDTH)
    
    i_table = [['Información del Equipo','','','Información de Mantenimiento','']]
    i_table.append(['Número de Equipo', 'asd', '    ','Lugar de Trabajo' ,' ']) # these are the other rows
    i_table.append(['Marca de Equipo', 'asd', '    ', 'Marca Aceite', 'asd'])
    i_table.append(['Modelo de Equipo', 'asd', '    ','Nombre Aceite' , 'asd'])
    i_table.append(['Serie de Equipo', 'asd', '    ', 'Visc en Etiqueta', 'asd'])
    i_table.append(['Horas/Km de Equipo', 'asd', '    ', '', 'asd'])
    i_table.append(['Componente', 'asd', '    ', 'PM', 'asd'])
    i_table.append(['Marca de Componente', 'asd', '    ', ' ',' '])
    i_table.append(['Modelo de Componente', 'asd', '    ', ' ',' '])
    i_table.append(['Nº serie de Componente', 'asd', '    ', ' ',' '])
    i_table.append(['O/T Cliente', 'asd', '    ', ' ',' '])
    i_table.append(['O/T Lubeman', 'asd', '    ', ' ',' '])
    
    #doc.add_table(i_table, 525)
    img_left = Image(request.folder + 'static/images/left.jpg', 115,82)
    logo = Image(request.folder + 'static/images/logo.png', 109,82)
    #doc.add_image(logo_path, 90, 100, pdf.LEFT)
    data1= [[img_left, 'Información del Equipo','','','Información de Mantenimiento:','',logo],
     ['','Número de Equipo:', 'CA-02', '                                 ','Lugar de Trabajo:' ,'SAN SIMON EQUIPOS-MINA LA VIRGEN',''],
     ['','Marca de Equipo:', 'Caterpillar', '    ', 'Marca Aceite:', 'Mobil',''],
     ['','Modelo de Equipo:', '777F', '    ','Nombre Aceite:' , 'HD',''],
     ['','Serie de Equipo:', 'JRP00408', '    ', 'Visc en Etiqueta:', '10W',''],
     ['','Horas/Km de Equipo:', 'asd', '    ', '', '',''],
     ['','Componente:', 'SISTEMA HIDRAULICO', '    ', 'PM:', '',''],
     ['','Marca de Componente:', 'asd', '    ', ' ',' ',''],
     ['','Modelo de Componente:', 'asd', '    ', ' ',' ',''],
     ['','Nº serie de Componente:', 'asd', '    ', ' ',' ',''],
     ['','O/T Cliente:', 'asd', '    ', ' ',' ',''],
     ['','O/T Lubeman:', 'TR09776', '    ', ' ',' ','']]
    t1=Table(data1,style=[
     ('SIZE',(0,0),(-1,-1),4),
     ('ALIGN',(0,0),(-1,-1),'LEFT'),
     ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
     ('RIGHTPADDING',(0,0),(-1,-1),2),
     ('LEFTPADDING',(0,0),(-1,-1),2),
     ('TOPPADDING',(0,0),(-1,-1),0),
     ('BOTTOMPADDING',(0,0),(-1,-1),-5),
     ('GRID',(0,0),(-1,-1),0.5,colors.grey),
     ('SPAN',(0,0),(0,11)),
     ('SPAN',(6,0),(6,11)),
     ])

    doc.add(t1)

    
    doc.add_spacer()
    data= [[Paragraph('TENDENCIA DEL COBRE SIGUE EN INCREMENTO Y ES ELEVADO. NIQUEL ESTARIA LIG. ALTO. REVISAR TEMPERATURAS DE OPERACION. REVISAR PARAMETROS DE OPERACION.\nREVISAR LOS BUJES DEL CONVERTIDOR DE TORQUE. REVISAR PRESIONES EN BOMBAS HIDRAULICAS. REVISAR FILTROS DE ACEITE. SE RECOMIENDA CAMBIAR ACEITE/FILTROS.\nENVIAR SGTE MUESTRA A LAS 50 HORAS POSTERIOR AL CAMBIO.',p), 'ESTADO:'],
     ['', 'PRECAUCIÓN']]
    t=Table(data,style=[
     ('SIZE',(0,0),(0,1),6.1),
     ('ALIGN',(0,0),(-1,-1),'LEFT'),
     ('RIGHTPADDING',(0,0),(-1,-1),2),
     ('LEFTPADDING',(0,0),(-1,-1),2),
     ('BACKGROUND',(1,1),(1,1),colors.yellow),
     ('SIZE',(1,0),(-1,-1),11),
     ('FONT',(1,0),(-1,-1),'Helvetica-Bold'),
     ('ALIGN',(1,0),(-1,-1),'CENTER'),
     ('SPAN',(0,0),(0,1)),
     ])

    doc.add(t)
    doc.add_spacer()
    
    doc.add_header('Resultados', pdf.H3)
    
    ir_table = [['Información de la Muestra','Elementos de Desgaste (partes por millón)','Contaminación','Condición del Aceite']] # this is the header row 
    doc.add_table(ir_table, 550)

    #data = db(db.tempo).select()
    #    for r in db(db.tempo).select():
    #    text += r.name_id + " " + r.kv + " " + r.fecha + " " + r.hora + " " + r.tecnico  + "\n"
    #aku_row = db(db.infra.name_sample==1001).select()
    for r in db(db.infra.name_sample==1001).select():
        textwater = r.water
        textoxi = r.oxi
        textsoot = r.sooth
        textsulfa = r.sulfa
        textnitra = r.nitra
    
    data= [['','# Muestra', 'Fechas', '02', 'Horas/Km\naceite', 'Horas/Km\ncomponente',
            'Fe', 'Al', 'Cu', 'Cr', 'Pb', 'Sn', 'Si', 'Na', 'K', 'Ca', 'Mg', 'P', 'Zn',
            'Agua %', 'Dilución %', 'Cód. ISO', 'Visc. 100 ºC',
            'Oxidación', 'Soot', 'Sulfatación', 'Nitración'],
     ['10', 'Toma', 'Recepción', 'Reporte', '', ''],
     ['7/30/2013', '20', '21', '22', '23', '24', '5.5', '0.6', '0.1', '11.4', '', '', '', '', '', '', '', '', '',textwater, '', '', '',textoxi,textsoot,textsulfa,textnitra],
     ['7/15/2013', '30', '31', '32', '33', '34'],
     ['7/15/2013', '40', '41', '42', '43', '44'],
     ['Proyectado', '30', '31', '32', '', '', '6.3', '0.7', '1.5', '0.1', '13.1']]
    t=Table(data,style=[
     ('SIZE',(0,0),(-1,-1),6.1),
     ('ALIGN',(0,0),(-1,-1),'CENTRE'),
     ('RIGHTPADDING',(0,0),(-1,-1),2),
     ('LEFTPADDING',(0,0),(-1,-1),2),
     ('TOPPADDING',(0,0),(-1,-1),0),
     ('BOTTOMPADDING',(0,0),(-1,-1),-5),
     ('GRID',(0,0),(-1,-1),0.5,colors.grey),
     ('BACKGROUND',(0,0),(0,0),colors.palegreen),
     ('BACKGROUND',(6,2),(18,4),colors.HexColor('#B8E68A')),
     ('FONT',(6,2),(-1,-1),'Helvetica-Bold'),
     ('BACKGROUND',(9,2),(9,2),colors.yellow),
     ('SPAN',(0,0),(0,1)),
     ('SPAN',(1,0),(3,0)),
     ('SPAN',(0,5),(3,5)),
     ])

    doc.add(t)

    graph1 = Image("https://chart.googleapis.com/chart?chs=200x125&cht=lc&chco=0077CC&chxt=y&chd=t:27,25,60,31,25,39,25,6,26,28,80,28,27,31,27,29,26,35,70,25&chm=H,FF0000,0,18,1", 75,30)
    graph2 = Image("https://chart.googleapis.com/chart?chs=200x125&cht=lc&chco=0077CC&chxt=y&chd=t:27,25,60,31,25,39,25,6,26,28,80,28,27,31,27,29,26,35,70,25&chm=H,FF0000,0,18,1&chtt=Actual", 75,40)
    graph3 = Image("https://chart.googleapis.com/chart?cht=lc&chd=s:cEAELFJHHHKUju9uuXUc&chco=76A4FB&chls=2.0,0.0,0.0&chs=200x125&chg=20,50,3,3,10,20&chxt=x,y&chxl=0:%7C0%7C1%7C2%7C3%7C4%7C5%7C1:%7C0%7C50%7C100&chtt=Histórico", 75,40)
    graph4 = Image("https://chart.googleapis.com/chart?cht=lc&chd=s:cEAELFJHHHKUju9uuXUc&chco=76A4FB&chls=2.0,0.0,0.0&chs=200x125&chg=20,50,3,3,10,20&chxt=x,y&chxl=0:%7C0%7C1%7C2%7C3%7C4%7C5%7C1:%7C0%7C50%7C100", 75,40)
    graph5 = Image("https://chart.googleapis.com/chart?cht=lc&chd=s:UVVUVVUUUVVUSSVVVXXYadfhjlllllllmmliigdbbZZXVVUUUTU&chco=0000FF&chls=2.0,1.0,0.0&chs=200x125&chxt=x,y&chxl=0:%7CJan%7CFeb%7CMar%7CJun%7CJul%7CAug%7C1:%7C0%7C25%7C50%7C75%7C100&chg=100.0,25.0&chf=c,ls,90,999999,0.25,CCCCCC,0.25,FFFFFF,0.25", 75,40)
    graph6 = Image("https://chart.googleapis.com/chart?cht=lc&chd=s:UVVUVVUUUVVUSSVVVXXYadfhjlllllllmmliigdbbZZXVVUUUTU&chco=0000FF&chls=2.0,1.0,0.0&chs=200x125&chxt=x,y&chxl=0:%7CJan%7CFeb%7CMar%7CJun%7CJul%7CAug%7C1:%7C0%7C25%7C50%7C75%7C100&chg=100.0,25.0&chf=c,ls,90,999999,0.25,CCCCCC,0.25,FFFFFF,0.25&chtt=ADITIVOS", 75,40)
    
    #doc.add(pdf.Table([[graph1,graph2]], style=[('VALIGN', (0,0), (-1,-1), 'TOP')]))

    doc.add_spacer()


    doc.add_header('Tendencias', pdf.H3)
    doc.add_spacer()
    #doc.add_paragraph("Desgaste")
    data= [['DESGASTE','','CONTAMINACIÓN','CONDICIÓN DEL ACEITE',''],
     [graph1,graph1,graph2,graph1,graph1],
     [graph1, graph1, '', graph5, graph5],
     [graph1, graph1, graph3, graph5, graph5],
     [graph1, graph1, graph4, graph6, graph5],
     [graph1, '', '', graph5, graph5]]
    t=Table(data,style=[
     ('SIZE',(0,0),(-1,-1),6.1),
     ('TEXTCOLOR',(0,0),(-1,-1),colors.HexColor('#B8B8B8')),
     ('ALIGN',(0,0),(-1,-1),'CENTRE'),
     ('RIGHTPADDING',(0,0),(-1,-1),2),
     ('LEFTPADDING',(0,0),(-1,-1),2),
     ('TOPPADDING',(0,0),(-1,-1),0),
     ('BOTTOMPADDING',(0,0),(-1,-1),0),
     ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#A34747')),
     ('SPAN',(2,1),(2,2)),
     ])

    doc.add(t)
    
    doc.add_spacer()
    #doc.add_paragraph("Contaminación")
    
    #tend2 = pdf.Image("https://chart.googleapis.com/chart?chs=200x125&cht=lc&chco=0077CC&chxt=y&chd=t:27,25,60,31,25,39,25,6,26,28,80,28,27,31,27,29,26,35,70,25&chm=H,FF0000,0,18,1", 250,150)
    #doc.add(tend2)
    
    #doc.add_spacer()
    #doc.add_paragraph("Condición del Aceite")
    
    #tend3 = pdf.Image("https://chart.googleapis.com/chart?cht=lc&chd=s:cEAELFJHHHKUju9uuXUc&chco=76A4FB&chls=2.0,0.0,0.0&chs=200x125&chg=20,50,3,3,10,20&chxt=x,y&chxl=0:%7C0%7C1%7C2%7C3%7C4%7C5%7C1:%7C0%7C50%7C100", 250,150)
    #doc.add(tend3)
    # all the rest I omitted here but you get the picture.

    # read the reportLab docs and the source below to figure out how to tewak things.

    # again, see http://www.reportlab.com/docs/reportlab-userguide.pdf

    # ...

    # ...

    header = {'Content-Type': 'application/pdf'}
    response.headers.update(header)
    return doc.render()

import cStringIO
 
from reportlab.platypus.doctemplate import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus.flowables import Image
from reportlab.platypus.tables import Table, TableStyle
