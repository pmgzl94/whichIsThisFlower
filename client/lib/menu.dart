import 'package:flutter/material.dart';
import 'package:graphql_flutter/graphql_flutter.dart';

final String logout = """
  mutation logout {
      logout(username: \$username) {
	ok
      }
  }
""";

AlertDialog a(context, mssg) {return AlertDialog(
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
class CreateMenu extends StatelessWidget {

  @override
  Widget build(BuildContext context) {
    return Scaffold(
	appBar: AppBar(title: Text('Menu')),
	body: Column(
	  children: [
	    Align (
	      alignment: Alignment(0.0, -0.75),
	      child: CreateMenuButton(),
	    ),
	  ]
	),
	backgroundColor: Color.fromRGBO(0, 200, 0, 0.6),
	// body: Center(child: RawWords()),
      // home: MyHomePage(title: 'Flutter Demeau Home Page'),
    );
  }
}

class CreateMenuButton extends StatefulWidget {

  @override
  CreateMenuButtonState createState() => CreateMenuButtonState();
}

class CreateMenuButtonState extends State<CreateMenuButton>
{
    final _id = GlobalKey<FormState>();
    bool state = false;

    void hasClicked() {
      this.state = true;
    }

    void quit(context) {
      Navigator.pop(context);
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
	       Mutation(
		  options: MutationOptions(
		    documentNode: gql(logout),
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
		      print("LOGOUT");
		      quit(context);
		    }
		  ),
		  builder: (RunMutation runMutation, QueryResult result) {
		    return Padding(
			padding: const EdgeInsets.symmetric(vertical: 16.0),
			child: ElevatedButton(
			  onPressed: () {
			    runMutation({"token": "token"});
			  },
			  child: Text('Logout'),
			)
		    );
		  }
		)
	      ]
	    )
	  );

    }
}

// class ButtonCreateMenu extends StatelessWidget {

//   @override
//   Widget build(BuildContext context) {
//       return ElevatedButton(
//               onPressed: () {
//                 Navigator.push(
//                 context,
//                 MaterialPageRoute(builder: (context) => CreateMenu()),
//                 );
//                },
//               child: Text('Sign Up'),
//             );
//   }
// }