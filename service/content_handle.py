# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 14:40
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : content_handle.py
# @Software: PyCharm
import re

diff_content = """@@ -41,42 +41,21 @@ import java.util.Optional;\n @RequestMapping(\"/settlementForm\")\n @RequiredArgsConstructor\n @Slf4j\n-@Tag(name=\"结算制单\")\n+@Tag(name = \"结算制单\")\n public class SettlementFormController extends BaseController {\n \n     private final OssFileService ossFileService;\n     private final SequenceService sequenceService;\n     private final SyncImportTaskRepo syncImportTaskRepo;\n     private final ImportAssist importAssist;\n-    private final SettlementBatchAutoRepo settlementBatchAutoRepo;\n     private final SettlementFormAssist settlementFormAssist;\n     private final RedissonClient redissonClient;\n \n     @PostMapping(value = \"/import\")\n     @Operation(summary = \"结算制单导入\")\n-    public ResponseMO importData(@RequestParam(value = \"file\") MultipartFile file){\n-        String fileName = file.getOriginalFilename();\n-        ResponseMO responseMO = FileValidateUtils.validateFile(fileName);\n-        if (responseMO.checkFailure()) {\n-            return responseMO;\n-        }\n-        try {\n-            OssFileBO fileVO = ossFileService.uploadFile(file, CommonConstants.FOLDER_PREFIX);\n-            SyncImportTaskDO syncImportTaskDO = new SyncImportTaskDO();\n-            syncImportTaskDO.setSequence(sequenceService.generateImportNumber(getCurrentTenantCode(), ImportType.SETTLEMENT_RECORD.name()));\n-            syncImportTaskDO.setFileKey(fileVO.getFileKey());\n-            syncImportTaskDO.setType(ImportType.SETTLEMENT_RECORD.name());\n-            syncImportTaskDO.setTenantId(this.getCurrentTenantId());\n-            syncImportTaskDO.setUserId(this.getCurrentUserIdDetermine());\n-            syncImportTaskDO.setUserName(getCurrentSystemUserInfo().getUserName());\n-            syncImportTaskDO.setHandler(SpringBeanUtils.fetchBeanName(SettlementFormImportAssist.class));\n-            syncImportTaskRepo.save(syncImportTaskDO);\n-            importAssist.createEvent(syncImportTaskDO.getId());\n-        } catch (UploadFileException e) {\n-            log.error(\"自招订单-上传文件出错:\" + e);\n-            return ResponseMO.errorWithMessage(\"上传文件出错!\");\n-        }\n-        return ResponseMO.success();\n+    public ResponseMO importData(@RequestParam(value = \"file\") MultipartFile file) {\n+\n+        return this.importData(file, ImportType.SETTLEMENT_RECORD, SettlementFormImportAssist.class);\n     }\n \n     @Operation(summary = \"提交结算制单\")\n@@ -92,7 +71,7 @@ public class SettlementFormController extends BaseController {\n             settlementFormAssist.commitTask(committedMO, this.getCurrentTenantId());\n         } catch (OperateUnSupportException e) {\n             return ResponseMO.errorWithMessage(\"这个批次已提交!\");\n-        }finally {\n+        } finally {\n             rLock.unlock();\n         }\n         return ResponseMO.success();\n
"""

import re


# def filter_diff_content(diff_content):
#     lines = diff_content.split('\n')
#     filtered_lines = [line for line in lines if not line.startswith('-')]
#     filtered_content = '\n'.join(filtered_lines)
#     filtered_content = re.sub(r'@@.*\n', '', filtered_content)
#     lines = filtered_content.split('\n')
#     processed_code = '\n'.join([line[1:] if line.startswith('+') else line for line in lines])
#     return processed_code


def filter_diff_content(diff_content):
    filtered_content = re.sub(r'(^-.*\n)|(^@@.*\n)', '', diff_content, flags=re.MULTILINE)
    processed_code = '\n'.join([line[1:] if line.startswith('+') else line for line in filtered_content.split('\n')])
    return processed_code


if __name__ == '__main__':
    print(filter_diff_content(diff_content))
