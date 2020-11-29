import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';

String createUser = """
  mutation CreateUser(\$username: String!, \$password: String!) {
      createUser(input: {username: \$username, password: \$password}) {
        ok
      }
  }
""";

// class CreateUserQuery extends StatelessWidget {
//   final String username;
//   final String password;

//   CreateUserQuery({@required this.username, @required this.password});
  
//   @override
//   Widget build(BuildContext context) {
//     return Mutation(
//       options: MutationOptions(
//           documentNode: gql(createUser),
//           variables: {"username": username, "password": password}
//       ),
//       builder: (RunMutation result, QueryResult,
//         FetchMore fetchMore}) {
//         if (result.hasException) {
//           return Text(result.exception.toString());
//         }
//         if (result.loading && result.data == null) {
//           return const Center(
//             child: CircularProgressIndicator(),
//           );
//         }
//         if (result.data["ok"] == false) {
//           return Text("Username already exists");
//         }
//         else {
//           //pop Navigator to get back to login page
//           return Text("User sucessfully created");

//         }
//       }
//     );
//   }
// }


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
    bool state = false;
    
    void hasClicked() {
      this.state = true;
    }

    final mc1 = TextEditingController();
    final mc2 = TextEditingController();

    @override
    void dispose() {
    // Clean up the controller when the widget is disposed.
      mc1.dispose();
      mc2.dispose();
      super.dispose();
    }

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
                  controller: mc1,
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
                  controller: mc2,
                ),
                
                Mutation(
                  options: MutationOptions(
                    documentNode: gql(createUser),
                    update: (Cache cache, QueryResult result) {
                      return cache;
                    },
                    onCompleted: (dynamic resultData) {
                      print(resultData);
                    },
                  ),
                  builder: (RunMutation runMutation, QueryResult result) {
                    return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 16.0),
                        child: ElevatedButton(
                        onPressed: () => runMutation({"username": mc1.text, "password": mc2.text}),
                        child: Text('Create Account'),
                        // Validate will return true if the form is valid, or false if
                        // the form is invalid.
                        // if (_id.currentState.validate()) {
                        // this.hasClicked();
                        // // call gql request
                        // }
                        )
                    );
                  }
                )
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