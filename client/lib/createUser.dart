import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';

final String createUser = """
  mutation CreateUser(\$username: String!, \$password: String!) {
      createUser(username: \$username, password: \$password) {
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

AlertDialog a(context, mssg) {
  return AlertDialog(
      title: Text('Error occured'),
      content: SingleChildScrollView(
        child: ListBody(
          children: <Widget>[
            Text(mssg),
          ],
        ),
      ),
      actions: <Widget>[
        TextButton(
          child: Text("Close"),
          onPressed: () {
            Navigator.of(context).maybePop();
          },
        ),
      ],
    );
}

class CreateUser extends StatelessWidget
{
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
            title: Text('Create User'),
            centerTitle: true,
            leading: IconButton(
                icon:Icon(
                      Icons.arrow_back,
                      color: Colors.black
                ),
                onPressed:() => Navigator.maybePop(context, false),
            ),
        ),
        body: Column(
          children: [
            Align (
              alignment: Alignment(0.0, -0.75),
              child: CreateUserForm(),
            ),
          ]
        ),
        // backgroundColor: Theme.of(context).primaryColor,
        // backgroundColor: Color.fromRGBO(0, 200, 0, 0.6),
        backgroundColor: Colors.white,
        // body: Center(child: RawWords()),
      // home: MyHomePage(title: 'Flutter Demeau Home Page'),
    );


  }
}

class CreateUserForm extends StatefulWidget
{
  @override
  CreateUserFormState createState() => CreateUserFormState();
}

class CreateUserFormState extends State<CreateUserForm>
{
    final _id = GlobalKey<FormState>();
    bool state = false;

    void hasClicked()
    {
        this.state = true;
    }

    void quit(context)
    {
        Navigator.maybePop(context);
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
                Padding(
                    padding: EdgeInsets.only(
                        left: 25.0, right: 25.0, top: 50.0),
                    child: new Row(
                      mainAxisSize: MainAxisSize.max,
                      children: <Widget>[
                        new Column(
                          mainAxisAlignment: MainAxisAlignment.start,
                          mainAxisSize: MainAxisSize.min,
                          children: <Widget>[
                            new Text(
                              'Username',
                              style: TextStyle(
                                  fontSize: 16.0,
                                  fontWeight: FontWeight.bold),
                            ),
                          ],
                        ),
                      ],
                    )
                  ),
                  Padding(
                    padding: EdgeInsets.only(left: 25.0, right: 25.0),
                    child: TextFormField(
                      decoration: const InputDecoration(
                          hintText: 'Enter your username',
                      ),
                      validator: (value) {
                          if (value.isEmpty) {
                            return 'Please enter your username';
                          }
                          return null;
                      },
                      controller: mc1,
                    ),
                  ),
                  Padding(
                    padding: EdgeInsets.only(
                        left: 25.0, right: 25.0, top: 25.0),
                    child: new Row(
                      mainAxisSize: MainAxisSize.max,
                      children: <Widget>[
                        new Column(
                          mainAxisAlignment: MainAxisAlignment.start,
                          mainAxisSize: MainAxisSize.min,
                          children: <Widget>[
                            new Text(
                              'Password',
                              style: TextStyle(
                                  fontSize: 16.0,
                                  fontWeight: FontWeight.bold),
                            ),
                          ],
                        ),
                      ],
                    )
                  ),
                  Padding(
                    padding: EdgeInsets.only(left: 25.0, right: 25.0),
                    child: TextFormField(
                      decoration: const InputDecoration(
                          hintText: 'Enter your password',
                      ),
                      validator: (value) {
                          if (value.isEmpty) {
                            return 'Please enter your password';
                          }
                          return null;
                      },
                      controller: mc2,
                      obscureText: true,
                    ),
                  ),
                  Mutation(
                    options: MutationOptions(
                      documentNode: gql(createUser),
                      update: (Cache cache, QueryResult result) {
                        return cache;
                      },
                      onError: (result) {
                        print("error");
                        print(result);
                      },
                      onCompleted: (dynamic resultData) {
                        print("on completed");
                        print(resultData.data);
                        if (resultData != null && resultData.data["createUser"] != null && resultData.data["createUser"]["ok"] == true) {
                          print(resultData.data["createUser"]["ok"]);
                          quit(context);
                        } else {
                          print("user already exist");
                          showDialog<AlertDialog>(
                            context: context,
                            builder: (BuildContext context) {
                              return a(context, "User already exists");
                          });
                        }
                      }
                    ),
                    builder: (RunMutation runMutation, QueryResult result) {
                      return Padding(
                          padding: const EdgeInsets.symmetric(vertical: 30.0, horizontal: 25),
                          child: ElevatedButton(
                            style: ElevatedButton.styleFrom(
                               shape: RoundedRectangleBorder(
                                 borderRadius: BorderRadius.circular(20),
                                 // borderRadius: BorderRadius.circular(10),
                               ),
                               minimumSize: Size(350, 40),
                          //      primary: Color.fromRGBO(0, 102, 0, 0.6),
                            ),
                            onPressed: () {
                              runMutation({"username": mc1.text, "password": mc2.text});
                            },
                            child: Text('Register'),
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
      return Padding(
                padding: const EdgeInsets.symmetric(vertical: 10.0, horizontal: 25),
                        child: ElevatedButton(
                          style: ElevatedButton.styleFrom(
                               shape: RoundedRectangleBorder(
                                 borderRadius: BorderRadius.circular(20),
                               ),
                               primary: Colors.white,
                               onPrimary: Colors.green,
                               textStyle: TextStyle(
                                    // fontSize: 30,
                                    fontWeight: FontWeight.bold
                               ),
                               minimumSize: Size(350, 40),
                          ),
              onPressed: () {
                Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => CreateUser()),
                );
              },
              child: Text('Sign Up'),
              )
            );
  }
}
