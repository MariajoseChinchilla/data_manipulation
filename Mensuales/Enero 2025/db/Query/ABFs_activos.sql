-- Declaración de las variables de fecha
DECLARE @FechaInicio DATE = '2024-01-01';
DECLARE @FechaFin DATE = CAST(GETDATE() AS DATE);
SELECT
	 [Fecha_Datos]				= [Rotacion de Empleados].Fecha	
	,[Numero de Antiguedad]		= Expediente.[Numero de Antiguedad]	
	--,[Nombre y Apellido]		= Expediente.[Nombre y Apellido]
	--,[Nombre del Puesto]		= [Puesto].[Nombre del Puesto]	
	,[Nombre Plaza]				= Plaza.[Nombre Plaza]
	,[Segmento]					= [Plaza].Segmento
FROM [BTMM-ModeloDeRentabilidadSostenida].[Modelo].[Rotacion de Empleados]	
	INNER JOIN [BTMM-ModeloDeRentabilidadSostenida].[Dimension].[Compania]
		ON [Rotacion de Empleados].KnCompania = Compania.KnCompania	
	INNER JOIN [BTMM-ModeloDeRentabilidadSostenida].[Dimension].[Expediente]
		ON [Rotacion de Empleados].KnExpediente = Expediente.KnExpediente	
	INNER JOIN [BTMM-ModeloDeRentabilidadSostenida].[Dimension].[Plaza]
		ON [Rotacion de Empleados].KnPlaza = Plaza.KnPlaza
	INNER JOIN [BTMM-ModeloDeRentabilidadSostenida].[Dimension].[Centro de Trabajo]
		ON [Rotacion de Empleados].KnCentroDeTrabajo = [Centro de Trabajo].KnCentroDeTrabajo
	INNER JOIN [BTMM-ModeloDeRentabilidadSostenida].[Dimension].[Puesto]
		ON [Rotacion de Empleados].KnPuesto = Puesto.KnPuesto	
	INNER JOIN [BTMM-ModeloDeRentabilidadSostenida].[Dimension].[Empleo]
		ON [Rotacion de Empleados].KnEmpleo = [Empleo].KnEmpleo
WHERE [Rotacion de Empleados].[Cantidad de Empleados] = 1
	AND [Rotacion de Empleados].[Bajas] = 0
	AND [Rotacion de Empleados].KnCompania IN (1, 6, 8, 9, 10)
	AND Compania.[Nombre Compania] IN('Ditca','Bantrab')
	AND [Plaza].Segmento IN('Centro De Negocios','Asesores De Bienestar Financiero','Otros Segmentos Comerciales')
	AND [Nombre Plaza] IN(
						 'Receptor Pagador'
						,'Asistente De Gestiones Crediticias'
						,'Asistente De Servicios Bancarios'
						,'Asesor De Bienestar Financiero'
						,'Asesor De Bienestar Financiero Bt'						
						)
	AND [Rotacion de Empleados].Fecha BETWEEN @FechaInicio AND @FechaFin
	--AND Expediente.[Numero de Antiguedad]	= '55111'
	ORDER BY 1 asc