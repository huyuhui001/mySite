# Windows 11在线账户强制政策全面升级

Microsoft is eliminating all known workarounds that let users install Windows 11 without an internet connection or Microsoft account, forcing everyone through the online setup process. The Verge reports:
微软正全面封杀那些允许用户在无网络连接或微软账户情况下安装Windows 11的变通方案，强制所有用户必须完成在线设置流程。据The Verge报道：

"We are removing known mechanisms for creating a local account in the Windows Setup experience (OOBE)," says Amanda Langowski, the lead for the Windows Insider Program. "While these mechanisms were often used to bypass Microsoft account setup, they also inadvertently skip critical setup screens, potentially causing users to exit OOBE with a device that is not fully configured for use."
"我们正在移除Windows初始化设置界面中已知的本地账户创建方法，"Windows Insider项目负责人阿曼达·兰戈夫斯基表示，"虽然这些方法常被用来跳过微软账户设置，但也会使用户错过关键设置步骤，可能导致设备未完成全面配置就退出初始化流程。"

The changes mean Windows 11 users will need to complete the OOBE screens with an internet connection and Microsoft account in future versions of the OS. Microsoft already removed the "bypassnro" workaround earlier this year, and today's changes also disable the "start ms-cxh:localonly" command that Windows 11 users discovered after Microsoft's previous changes. Using this command now resets the OOBE process and it fails to bypass the Microsoft account requirement.
此举意味着未来版本的Windows 11用户必须连接互联网并登录微软账户才能完成系统初始化设置。今年早些时候微软已禁用"bypassnro"绕过命令，而最新调整还封堵了用户后来发现的"start ms-cxh:localonly"命令。现在使用该命令只会重置初始化流程，仍无法避开微软账户要求。
