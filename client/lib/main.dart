import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';

void main() {
  runApp(MyApp());
  print("hello");
}

//carefull alignment is between 1 and -1

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demeau(is the widget title)',
      theme: ThemeData(
        primarySwatch: Colors.green,
      ),
      home: Scaffold(
        appBar: AppBar(title: Text('Login')),
        body: Container(
          child: Align (
            alignment: Alignment(0.0, -0.75),
            child: RawWords(),
          )
        ),
        backgroundColor: Color.fromRGBO(0, 200, 0, 0.6),
        // body: Center(child: RawWords()),
      ),
      // home: MyHomePage(title: 'Flutter Demeau Home Page'),
    );
  }
}

class RawWords extends StatefulWidget {
  @override
  RawWordState createState() => RawWordState();
}

class RawWordState extends State<RawWords>
{
  final _username = GlobalKey<FormState>();
  final _mdp = GlobalKey<FormState>();
  @override
  Widget build(BuildContext context) {
    // final word = "on est laaaa";
    // return Text(word);
    return Form(
      key: _username,
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
                if (_username.currentState.validate() 
                  && _mdp.currentState.validate()) {
                  // call gql request
                }
              },
              child: Text('Login'),
            ),
          ),
        ]
      )
        
    );

  }
}

//Stateless widgets are immutable, meaning that their properties can’t change—all values are final.

