import 'package:flutter/material.dart';

class CreateUser extends StatelessWidget {
  
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'WITF: Create User',
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: Scaffold(
        appBar: AppBar(title: Text('Create User')),
        body: Column(
          children: [
            Align (
              alignment: Alignment(0.0, -0.75),
              child: CreateUserForm(),
            ),
          ]
        ),
        backgroundColor: Color.fromRGBO(0, 200, 0, 0.6),
        // body: Center(child: RawWords()),
      ),
      // home: MyHomePage(title: 'Flutter Demeau Home Page'),
    );
    
    
  }
}

class CreateUserForm extends StatefulWidget {
  @override
  CreateUserFormState createState() => CreateUserFormState();
}

class CreateUserFormState extends State<CreateUserForm>
{
    final _id = GlobalKey<FormState>();
    
    @override
    Widget build(BuildContext context) {
      return Form(
            key: _id,
            child: Column(
              children: <Widget> [
                TextFormField(
                  decoration: const InputDecoration(
                    hintText: 'username',
                  ),
                  validator: (value) {
                    if (value.isEmpty) {
                      return 'Please enter your username';
                    }
                    return null;
                  },
                ),
                TextFormField(
                  decoration: const InputDecoration(
                    hintText: 'password',
                  ),
                  validator: (value) {
                    if (value.isEmpty) {
                      return 'Please enter your password';
                    }
                    return null;
                  },
                ),
                
                Padding(
                  padding: const EdgeInsets.symmetric(vertical: 16.0),
                  child: ElevatedButton(
                    onPressed: () {
                      // Validate will return true if the form is valid, or false if
                      // the form is invalid.
                      if (_id.currentState.validate()) {
                        // call gql request
                      }
                    },
                    child: Text('Create Account'),
                  ),
                ),

              ]
            )
          );

    }

  
}

class ButtonCreateUser extends StatelessWidget {
  
  @override
  Widget build(BuildContext context) {
      return ElevatedButton(
              onPressed: () {
                Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => CreateUser()),
                );
              },
              child: Text('Sign Up'),
            );
  }
}