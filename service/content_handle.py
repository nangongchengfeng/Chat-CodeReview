# -*- coding: utf-8 -*-
# @Time    : 2023/7/14 14:40
# @Author  : 南宫乘风
# @Email   : 1794748404@qq.com
# @File    : content_handle.py
# @Software: PyCharm
import re

diff_content = """@@ -16,12 +16,12 @@ public class LaborAuthFilter implements Filter {

     @Override
     public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
-            HttpServletRequest servletRequest = (HttpServletRequest) request;
+        HttpServletRequest servletRequest = (HttpServletRequest) request;
         String userId = servletRequest.getHeader(USER_ID_KEY);
         String tenantId = servletRequest.getHeader(TENANT_ID_KEY);
         String openid = servletRequest.getHeader(OPENID_KEY);
         try {
-            if (StringUtils.hasText(tenantId)) {
+            if (StringUtils.hasText(userId) || StringUtils.hasText(tenantId)) {
                 LaborAuthentication laborAuthentication = new LaborAuthentication(userId, tenantId, openid);
                 LaborAuthenticationHolder.set(laborAuthentication);
             }
"""

lines = diff_content.split('\n')
filtered_lines = [line for line in lines if not (line.startswith('+') or line.startswith('-'))]
filtered_content = '\n'.join(filtered_lines)
# 使用正则表达式删除行
filtered_content = re.sub(r'@@.*\n', '', filtered_content)

print(filtered_content)
