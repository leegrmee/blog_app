-- DropForeignKey
ALTER TABLE "CategoryToArticle" DROP CONSTRAINT "CategoryToArticle_articleId_fkey";

-- AddForeignKey
ALTER TABLE "CategoryToArticle" ADD CONSTRAINT "CategoryToArticle_articleId_fkey" FOREIGN KEY ("articleId") REFERENCES "Article"("id") ON DELETE CASCADE ON UPDATE CASCADE;
