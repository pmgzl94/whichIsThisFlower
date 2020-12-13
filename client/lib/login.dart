import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';
import 'sharedPref.dart';
import './menu.dart';

//  mutation login(\$username: String!, \$password: String!) {
final String login = """
  mutation Login(\$username: String!, \$password: String!) {
      auth(username: \$username, password: \$password) {
	accessToken
      }
  }
""";

setToken(String token) async {
  SharedPreferences prefs = await SharedPreferences.getInstance();

  print('SET Token = $token');
  await prefs.setString('token', token);
}

// to call : str = await getToken()
Future<String> getToken() async {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  String token = prefs.getString('token');

  print('GET Token = $token');
  return token;
}

AlertDialog dialog(context, mssg) {return AlertDialog(
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
	Navigator.of(context).pop();
      },
    ),
  ],
);
}

class CreateLogin extends StatefulWidget {
  @override
  CreateLoginState createState() => CreateLoginState();
}

class CreateLoginState extends State<CreateLogin>
{
    final _id = GlobalKey<FormState>();
    bool state = false;

    void hasClicked()
    {
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
		  obscureText: true,
		),
		Mutation(
		  options: MutationOptions(
		    documentNode: gql(login),
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
		      print("print 1");
		      print(resultData.data["auth"]);
		      print("print 2");
		      print(resultData.data["auth"]["accessToken"]);
		      print("print 3");
		      if (resultData != null) {
		      	print("print INSIDE");
			print(resultData.data["auth"]["accessToken"]);
			print("OUAIS OUAIS OUAIS CA SET ICI");
			setToken(resultData.data["auth"]["accessToken"]);
			print("SET FINI LOL");
			print(getToken());
			print("GET ENDED");
			Navigator.push(
			  context,
			  MaterialPageRoute(builder: (context) => CreateMenu()),
			);
		      } else {
			print("User doesn't exist");
			showDialog<AlertDialog>(
			  context: context,
			  builder: (BuildContext context) {
			    return dialog(context, "User doesn't exist");
			});
		      }
		    }
		  ),
		  builder: (RunMutation runMutation, QueryResult result) {
		    return Padding(
			padding: const EdgeInsets.symmetric(vertical: 16.0),
			child: ElevatedButton(
			  onPressed: () {
			    runMutation({"username": mc1.text, "password": mc2.text});
			  },
			  child: Text('Login'),
			)
		    );
		  }
		)
	      ]
	    )
	  );

    }


}

class ButtonCreateLogin extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
      return ElevatedButton(
	      onPressed: () {
		Navigator.push(
		context,
		MaterialPageRoute(builder: (context) => CreateLogin()),
		);
	      },
	      child: Text('Login'),
	    );
  }
}