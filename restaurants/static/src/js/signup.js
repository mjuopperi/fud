var SignUpForm = React.createClass({
  handleSubmit: function(e) {
    e.preventDefault();

    $.ajax({
      type: 'POST',
      url: '/api/auth/register/',
      data: {
        username: this.refs.username.getDOMNode().value.trim(),
        email: this.refs.email.getDOMNode().value.trim(),
        password: this.refs.password.getDOMNode().value.trim()
      },
      success: function() {
        console.log('success')
      }
    });
  },
  render: function() {
    return (
      <form onSubmit={ this.handleSubmit }>
        <label htmlFor='username'>Username</label>
        <input type='text' name='username' ref='username'></input>
        <label htmlFor='email'>Email</label>
        <input type='email' name='email' ref='email'></input>
        <label htmlFor='password'>Password</label>
        <input type='password' name='password' ref='password'></input>
        <button type='submit'>Sign up</button>
      </form>
    );
  }
});

$(function() {
  React.render(<SignUpForm />, document.getElementById('signup-form'));
});
