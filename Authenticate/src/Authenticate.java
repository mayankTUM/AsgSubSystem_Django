import javax.naming.Context;
import javax.naming.Name;
import javax.naming.NamingEnumeration;
import javax.naming.NamingException;
import javax.naming.directory.*;
import javax.naming.ldap.InitialLdapContext;
import javax.naming.ldap.LdapContext;
import javax.naming.ldap.LdapName;
import javax.naming.ldap.StartTlsRequest;
import javax.naming.ldap.StartTlsResponse;

import java.io.IOException;
import java.util.Hashtable;

/**
 * User: gmc
 * Date: 16/02/11
 */
public class Authenticate {


	@SuppressWarnings({ "unchecked", "rawtypes", "unused" })
	public static void main(String[] args) throws NamingException {

		final String ldapAdServer = "ldaps://iauth.tum.de:636/cn="+args[0]+",ou=users,ou=data,ou=prod,ou=iauth,dc=tum,dc=de";
		final String ldapUsername = "cn="+args[0]+",ou=users,ou=data,ou=prod,ou=iauth,dc=tum,dc=de";
		final String ldapPassword = args[1];

		Hashtable env = new Hashtable();
		env.put(Context.SECURITY_AUTHENTICATION, "simple");
		if(ldapUsername != null) {
			env.put(Context.SECURITY_PRINCIPAL, ldapUsername);
		}
		if(ldapPassword != null) {
			env.put(Context.SECURITY_CREDENTIALS, ldapPassword);
		}
		env.put(Context.INITIAL_CONTEXT_FACTORY, "com.sun.jndi.ldap.LdapCtxFactory");
		env.put(Context.PROVIDER_URL, ldapAdServer);
		env.put(Context.REFERRAL, "throw");
		DirContext ctx = null;
		try
		{
			ctx = new InitialDirContext(env);
			NamingEnumeration<SearchResult> results = null;
			SearchControls controls = new SearchControls();
	        controls.setSearchScope(SearchControls.SUBTREE_SCOPE);
	        results = ctx.search("", "(objectClass=*)", controls);
	        while (results.hasMoreElements()) 
	        {
	        	SearchResult searchResult = (SearchResult) results.next();
	            Attributes attributes = searchResult.getAttributes();
	            Attribute attr1 = attributes.get("cn");
	            Attribute attr2 = attributes.get("fullName");
	            Attribute attr3 = attributes.get("imHauptEMail");
	            Attribute attr4 = attributes.get("imMatrikelNr");
	            System.out.print(attr1.get().toString()+":");
	            System.out.print(attr2.get().toString()+":");
	            System.out.print(attr3.get().toString()+":");
	            System.out.print(attr4.get().toString());
	        }
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}
}