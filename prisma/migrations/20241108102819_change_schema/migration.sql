/*
  Warnings:

  - Added the required column `user_id` to the `file` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "file" ADD COLUMN "user_id" INTEGER NOT NULL DEFAULT 1;

-- AddForeignKey
ALTER TABLE "file" ADD CONSTRAINT "file_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "user"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
