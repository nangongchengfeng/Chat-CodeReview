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
