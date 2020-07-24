import textwrap

FETCH_LOAD_MANAGER_DETAILS_SQL = textwrap.dedent("""
                                  SELECT ztLoadManagerTargetItemDetails.[ID]
                                      ,webConsoleAllTargetStructureSel.[Wave]
                                      ,webConsoleAllTargetStructureSel.[ProcessArea]
                                      ,webConsoleAllTargetStructureSel.[Object]
                                      ,webConsoleAllTargetStructureSel.[Target]
                                      ,ztLoadManagerTargetItemDetails.[WaveProcessAreaObjectTargetID]
                                      ,ztLoadManagerTargetItemDetails.[LoadCycle]
                                      ,ztLoadType.[LoadType]
                                      ,ztLoadManagerTargetItemDetails.[Version]
                                      ,ztParam.ReportPath 
                                  FROM [dspDMCC].[dbo].[ztLoadManagerTargetItemDetails] AS ztLoadManagerTargetItemDetails
                                            INNER JOIN [dspDMCC].[dbo].[ztLoadType] AS ztLoadType
                                            ON ztLoadManagerTargetItemDetails.LoadType = ztLoadType.ID
                                            INNER JOIN [dspDMCC].[dbo].webConsoleAllTargetStructureSel as webConsoleAllTargetStructureSel
                                            ON webConsoleAllTargetStructureSel.WaveProcessAreaObjectTargetID = ztLoadManagerTargetItemDetails.WaveProcessAreaObjectTargetID 
                                            CROSS JOIN Console.dbo.ztParam as ztParam
                                  WHERE ztLoadManagerTargetItemDetails.ID = {ID} 
                                                 """)

FETCH_SHAREPOINT_DETAILS_SQL = textwrap.dedent("""
                                  SELECT   TOP 1  [ID], [Name], [SiteURL], [SiteID], [ClientID], [ClientSecret], [FolderURL], [BaseFolderName]
                                  FROM            [dspDMCC].[dbo].[ztSharepoint]
                                                 """)

FETCH_TARGET_REPORT_DETAILS_SQL = textwrap.dedent("""
                                  SELECT        WaveProcessAreaObjectTargetReportID, TargetReport, ReportType, FileLocation, SegmentByField
                                  FROM            dspDMCC.dbo.webConsoleTargetReportStructureSel
                                  WHERE CAST(WaveProcessAreaObjectTargetID AS NVARCHAR(50)) = '{WaveProcessAreaObjectTargetID}' 
                                        AND RecordCount > 0
                                                 """)

FETCH_TARGET_REPORT_SEGMENT_DETAILS_SQL = textwrap.dedent("""
                                  SELECT        SegmentByValue, FileLocation
                                  FROM            DSW.dbo.ttWaveProcessAreaObjectTargetReportSegment
                                  WHERE CAST(WaveProcessAreaObjectTargetReportID AS NVARCHAR(50)) = '{WaveProcessAreaObjectTargetReportID}'
                                                 """)