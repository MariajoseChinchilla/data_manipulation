WITH DATOS AS (
    SELECT 
p.[KnNoPrecalificacion] AS PRECALIFICACION,
s.[referenciasib] AS REFERENCIA_SIB,
p.[KdFechaCarga] AS FECHA_SOLICITUD,
r.[DxColorDeudorOfertaComercial] AS RESULTADO,
p.[DxEjecutivoAsignado] AS ABF_ASIGNADO,
p.[DxNombreCompletoCliente] AS NOMBRE_CLIENTE,
p.[DxDpi] AS DPI, 
p.[DxNit] AS NIT,
p.[DxFechaNacimiento] AS FECHA_NACIMIENTO,
'COMPRA SALDO' AS PRODUCTO, 
-- datos de la segunda parte del dictamen
r.[DfMonto] AS MONTO,
r.[DfTasa] AS TASA,
r.[DfPlazo] AS PLAZO,
p.[DxTipoCliente] AS TIPO_CLIENTE,
p.[DfIngresosValidados] AS INGRESOS_VALIDOS,
r.[DfRciInternoFinalDeudor] AS RCI_INTERNO, 
r.[DfRciGlobalFinalDeudor] AS RCI_GLOBAL,
--- la mora detallarla por credito con fecha
d.[outDiasMoraInterno] AS MORA, 
d.[outCategoriaRiesgo] AS CATEGORIA,
d.[outSumaCuotaCreditosVigentesBT] AS CUOTAS_INTERNAS,
r.[DfCuotaMensualCreditoSinAhorro] AS NUEVA_CUOTA,
d.[outCuotaFiduciarioExterna] AS CUOTAS_EXTERNAS
-- pegar el color de la preca
FROM [Horus].[iniciativa_compra_saldo_externo] p 
LEFT JOIN  [silver].[pr_bit_ofergrupo_per_sircruta15_infgral] s 
on s.[no_precalificacion] = p.[KnNoPrecalificacion]
LEFT JOIN [Horus].[resultante_precalificaciones_goc] r 
ON r.[KnNoPrecalificacion] = p.[KnNoPrecalificacion]
LEFT JOIN [silver].[pr_bit_ofergrupo_per_participante] d 
ON d.[no_precalificacion] = p.[KnNoPrecalificacion]
WHERE r.[DxColorDeudorOfertaComercial] = 'APROBADO'
    AND r.[DxColorDeudorPersona] = 'APROBADO'
    AND r.[DxColorDeudorFinal] = 'APROBADO'
    AND p.[KdFechaCarga] >= '2024-12-15'
),

DETALLE AS (
--- para la mora y la exposicion
SELECT 
f.[descripcion] AS NOMBRE_PRUCTO,
f.[saldo] AS SALDO_CREDITO,
f.[cuotasPagadas] AS CUOTAS_PAGADAS,
((f.[capitalOriginal] - f.[saldo]) / f.[capitalOriginal]) AS PORCENTAJE_PAGADO
FROM [silver].[pr_bit_ofergrupo_per_burointernobantrab_datoscreditos] f 
WHERE f.[estado] = 'ACT'
)


SELECT TOP 10 * FROM DETALLE
SELECT TOP 10 * FROM DATOS