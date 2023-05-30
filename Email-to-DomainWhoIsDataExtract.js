/** Logins to a database, searches table for emails that arent gmail, yahoo, aol, outlook (as you can see) - removes the beginning name@ , leaving the domain name,
//    and does basic who is querys attempting to extract information usable, PoC -- abd for large enails list, this is actually pretty effect more then I would of originally thought.
//    Pretty slow, but that could be fixed easily. */

const { Sequelize, DataTypes } = require('sequelize');
const whois = require('whois');
const sequelize = new Sequelize('', '', '', {
  host: '',
  dialect: 'mysql',
  port: 3306,
  logging: console.log
});
const Account = sequelize.define('accounts_dedup', {
  email: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  accountNumber: {
    type: DataTypes.STRING,
    allowNull: false,
  },
  postalCode: {
    type: DataTypes.STRING
  }
}, {
  tableName: 'accounts_dedup',
  timestamps: false
});
async function processAccount(account) {
  // Check if the postalCode field is already filled
  if (account.postalCode) {
    console.log(`Skipping account ${account.accountNumber} - Postal code already filled.`);
    console.log('---');
    return;
  }
  const domain = extractDomainFromEmail(account.email);
  const lowerCaseDomain = domain.toLowerCase();
  const freeEmailProviders = [
    'gmail.com',
    'yahoo.com',
    'aol.com',
    'outlook.com',
    'hotmail.com',
    'mail.com'
  ];
  if (freeEmailProviders.some(provider => lowerCaseDomain.includes(provider))) {
    return;
  }
  try {
    const result = await performWhoisLookup(domain);
    const postalCode = extractPostalCodeFromWHOIS(result);
    if (postalCode) {
      console.log(`Account Number: ${account.accountNumber}`);
      console.log(`Domain: ${domain}`);
      console.log(`Postal Code: ${postalCode}`);
      console.log('---');

      await Account.update({ postalCode }, { where: { accountNumber: account.accountNumber } });
    }
  } catch (error) {
    console.error(`Error searching domain ${domain}: ${error}`);
  }
}

// Perform WHOIS lookup for a single domain
function performWhoisLookup(domain) {
  return new Promise((resolve, reject) => {
    whois.lookup(domain, { timeout: 5000 }, (error, result) => {
      if (error) {
        reject(error);
      } else {
        resolve(result);
      }
    });
  });
}

// Extract the domain from an email address
function extractDomainFromEmail(email) {
  const [, domain] = email.split('@');
  return domain ? domain.trim() : '';
}

// Extract the postal code from WHOIS data
function extractPostalCodeFromWHOIS(whoisData) {
  const matches = whoisData.match(/Postal Code: (.*)/i);
  return matches ? matches[1] : null;
}

// Fetch domains from the database and perform WHOIS lookup
async function fetchDomainsFromDatabase() {
  try {
    await sequelize.authenticate();
    console.log('Database connection has been established successfully.');

    const accounts = await Account.findAll();

    for (const account of accounts) {
      await processAccount(account);
    }

    console.log('Process completed successfully.');
  } catch (error) {
    
    console.error('Unable to connect to the database:', error);
  } finally {
    await sequelize.close();
  }
}

// Run the script
fetchDomainsFromDatabase();
