# 1. Introduction to HTML forms

Forms in web pages provide a structured way for users to input data direct, allowing applications to
collect and store user information.

An HTML [form](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/form) starts with a `<form>` element.

The `<form>` element is a container for different types of input elements, such as: text fields,
checkboxes, radio buttons, submit buttons, etc.

The `<form>` has attributes:

- The `action` attribute defines the action to be performed when the form is submitted, the
  URL processes the form submission
- The `method` attribute specifies the HTTP method to be used when submitting the form data. The
  form-data can be sent as URL variables (with method="get") or as HTTP post transaction (with
  method="post"). The default HTTP method when submitting form data is GET.

A form can contain the following HTML elements:

- `<input>` types include `<input type="button">`
  `<input type="checkbox">`
  `<input type="color">`
  `<input type="date">`
  `<input type="datetime-local">`
  `<input type="email">`
  `<input type="file">`
  `<input type="hidden">`
  `<input type="image">`
  `<input type="month">`
  `<input type="number">`
  `<input type="password">`
  `<input type="radio">`
  `<input type="range">`
  `<input type="reset">`
  `<input type="search">`
  `<input type="submit">`
  `<input type="tel">`
  `<input type="text">` (default value)
  `<input type="time">`
  `<input type="url">`
  `<input type="week">`
- `<label>` usually used for text associated with an input
- `<select>` dropdown
- `<textarea>` a longer text entry box
- `<button>` - types include button, reset and submit
- `<fieldset>`
- `<legend>`
- `<datalist>`
- `<output>`
- `<option>` options e.g. for a dropdown
- `<optgroup>` groups together options

Use relevant references to find the range of attributes that can be configured for each of the 
above:

- [Mozilla](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Forms)
- [W3Schools](https://www.w3schools.com/html/html_forms.asp)

Forms can be styled using Bootstrap or other styling. [Boostrap](https://getbootstrap.com/docs/5.3/forms/overview/) gives examples of how to apply
styles to achieve different form layouts.

[Next activity (Dash)](2-form-dash.md)

[Next activity (Flask](2-form-flask.md)

[Next activity (Streamlit)](2-form-streamlit.md)