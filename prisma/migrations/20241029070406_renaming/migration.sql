/*
  Warnings:

  - You are about to drop the column `hashed_password` on the `user` table. All the data in the column will be lost.
  - You are about to drop the column `user_name` on the `user` table. All the data in the column will be lost.
  - Added the required column `hashedpassword` to the `user` table without a default value. This is not possible if the table is not empty.
  - Added the required column `username` to the `user` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "user" DROP COLUMN "hashed_password",
DROP COLUMN "user_name",
ADD COLUMN     "hashedpassword" TEXT NOT NULL,
ADD COLUMN     "username" TEXT NOT NULL;
