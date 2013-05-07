MavensMate
==========

MavensMate is a tool that powers open source Force.com IDEs in various text editors across various platforms

### Wait...I'm confused. I thought MavensMate was a plugin for Sublime Text?

OK, it *WAS*. But now, we've rewritten MavensMate to be a cross-platform, text editor agnostic tool for developing Force.com applications. The [Sublime Text plugin][MMST2] still exists, it just utilizes the newly rewritten APIs in this project.

### What is mm?

`mm` is the executable that performs the heavy lifting. It can create new projects, compile code, move code between orgs, run apex tests, etc...and it's all JSON-based. Simply feed it JSON to provide context to your request, and it will respond in JSON. Here's an example:

##### Request

```
$ mm -o compile_project <<< '{ "project_name" : "myproject" }'
```

##### Response

```
{
	"success" : true,
	"body"	  : "Your operation completed successfully"	
}
```

For more information on mm's capabilities, head over to the [README][mmreadme]

### What is mmserver?

`mmserver` is a local http server that the out-of-box MavensMate UI uses to interact with the `mm` tool. The OOB MavensMate UI is written in HTML/CSS/JS, so to maintain a solid user experience, it makes Ajax calls to a local web server which in turns makes all the terminal calls to `mm`. If you're writing a MavensMate plugin, your UI can use `mmserver` or you can simply call `mm` directly from your plugin's UI.

### How can I write a plugin?

Pick your favorite text editor with extension capability and utilize the `mm` and `mmserver` tools to build fully-functional Force.com IDEs



[MMST2]: https://github.com/joeferraro/MavensMate-SublimeText
[mmreadme]: https://github.com/joeferraro/MavensMate/tree/master/mm#mm