/* Here we import some packages that will be used in the software */

import javax.naming.NamingEnumeration;
import javax.naming.directory.SearchControls;
import javax.naming.directory.SearchResult;
import javax.naming.ldap.InitialLdapContext;
import java.util.Hashtable;
import javax.naming.NamingException;

/* The comments of the LDAPInfo class coontain explanation of the functionalities*/

public class LDAPInfo {
  public static void main(String[] args) throws Exception {
    if (args.length < 1) {
      throw new RuntimeException("I need UID!"); // Command line agrument is obligatory
    }

    String uid = args[0]; // UID is taken from command line agrument

    String query = String.format("(&(uid=%s)(objectClass=person))", uid); // query is constructed based on command line
                                                                          // argument.
    System.out.println("LDAP Query: " + query); // the query is printed out upon call

    Hashtable<String, Object> env = new Hashtable<>();
    env.put("java.naming.provider.url", "ldap://localhost:8080/dc=example,dc=org");
    env.put("java.naming.factory.initial", "com.sun.jndi.ldap.LdapCtxFactory");
    InitialLdapContext ctx = new InitialLdapContext(env, null); // Connection ot LDAP is established

    SearchControls constraints = new SearchControls();
    constraints.setSearchScope(SearchControls.SUBTREE_SCOPE);
    constraints.setRuntimeAttributes(new String[] { "telephoneNumber" }); // we
    // want to extract telephonoe number

    NamingEnumeration<SearchResult> results = ctx.search("", query, constraints);

    try {
      if (!results.hasMore()) {
        System.out.println("Nobody found!");
      } else {
        Object phone = results.next().getAttributes().get("telephoneNumber");
        System.out.println("Phone : " + phone); // otherwise print the phone number
      }
    } catch (NamingException e) {
      // exception declaration
    } finally {
      results.close(); // Close the result handle
    }
  }
}
