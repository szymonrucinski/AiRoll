import firebase from "firebase";

const config = {
  type: "service_account",
  project_id: "image-classifier-bfcf5",
  private_key_id: "e359f9a1da994f0784c11c4d7ab720271bfc0181",
  private_key:
    "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQChkOFmUYJvvENP\nWGP1hBzUl6oj+fmWtYVhIJCbENKTr1hZquY4RgNpP62R6N4v75AhOzlcSQMtHyQ5\nVHnJ/UKeEsp03J4A/z5TG0UfldkHY3Hosoz41RSStH2qY8lJMxfFik8niEtRlO1D\nbTUkBGtM0e5+jn786Y9zzqp1gExS61rW/4nzyK1VC8fqKtk6P7dS8R7+DXnXFeIL\nqtdxGJ7MN4Bhp2o4GjJyUAI01u/IVW6TaTZPRPtLAzF6WCgf2iRnozD5GZ5Sa3If\nG6fiBy2AjI1J1yswV+biYDnAD8DaXD5DkJhCwj2UJoM0YnzG84rxB1DxfDOeP49p\nAQ9yXUzVAgMBAAECggEAIYQ4Ni0nlX1lK0MnbWnMP0/9NDxpyhl7A3Spevmo7Yk9\nF1DsNHVVxNI4dCHuYdxdNn+ePSZKWeRxc9Ex+LSoyrkUNd0EjClnKP9pvg0seitn\nmIHd28r8WxjFTwEnYx+NyWWRWR6dnV17QPcZRJEEH2oXgzqVXmsnXrtbQkfszXCA\nRPUXoWJul/1KF87WBc+Z0z/525Zr3dAW0fRYkzcMLiMthGriUujQJp6gnDT27y+v\nxZolttcLqKIoy9D4RuYX2H8jXHGgkZoh3oW+C5RVOUyjhZkR/LG+pwz7X5iMp8o4\nDiQe2sDQAcSqALOP5ryeyYRi2Sfahi0uBgGsYhNTmwKBgQDLamY7Ci6ady1hix3Z\ni+dD5iGnOdsYl/ZzWR74xvTMM5gHSfOPrMi85P5WGeO2uen4w5TyCJV+qyQRZyv2\nhhrJVXnwrpr9WLyypSZfBnwI9+xjLbpF7Rn3blhbfztWS2qw6KzsDzeY4qW/+b2g\nEdJiSBqQlQDThxqNNCE5847LuwKBgQDLVPXwicapuQfQfAzJEANdtS1LZJLy/Ah+\nyWI8k67h5FI9ZoQw5sDAWFh+Zi7YOxm6/KeplwIj245RlpScyDP0VYZgW0Wtjwbt\nonfgi0iyOaMr1ApMsIaG56SW9lmfZc/0EIlnItryhlBO/HBMA5e9IUM19jRMjdC2\no6L/QUuYrwKBgA635inDdNfMY8Y5ELHbA6LQFgNJlmbTKAv0mN8bVj8oRInSegMd\nV3EDiLumJ+nizeEoFbDlmhuOOo/fzTiLP4jt3GLj32cRcqXieUJK79KeTcZnWqEQ\npN5YZ6BHNn3p+xBN5aU2/KjdTWz0nxnj8DsYSIPJpEOp9Ovep8DPtLddAoGBAIbH\n8KbbjRagEi/+qrL0rGaHXFjneAkdS7xPXZDuDDSsll8g/2sy6n4VkcNnlJG8y1eJ\ndtIRyVdfiD1I5YXvp5DEyGhC2DMt5dfLpE7xxORvFFxPF+yx7tqp3g47ijkA0hHk\njFATaLLumXliGEYq84Bo9hZk91Hvh3QpkDhHXgb9AoGABzWiX4SBi3r0rPG4vKqE\nHaWExRJx5nGCa4ri/SD1K4cMsZb8OUoXPcZmxgL0/LZI9lQSkfEftYxRsWPzqyiQ\n+4knhZ+ua1BdhyDTXWkPq3Kqa0pA+1uNEaUTghrI65DedC5N+hG2lkOVy+G0iY8h\nLix5Xfr3DCXKv0wgkggmC3Y=\n-----END PRIVATE KEY-----\n",
  client_email: "image-classifier-bfcf5@appspot.gserviceaccount.com",
  client_id: "103597759144319125973",
  auth_uri: "https://accounts.google.com/o/oauth2/auth",
  token_uri: "https://oauth2.googleapis.com/token",
  auth_provider_x509_cert_url: "https://www.googleapis.com/oauth2/v1/certs",
  client_x509_cert_url:
    "https://www.googleapis.com/robot/v1/metadata/x509/image-classifier-bfcf5%40appspot.gserviceaccount.com",
};
firebase.initializeApp(config);

export default firebase;
